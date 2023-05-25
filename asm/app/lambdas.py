import json

import grpc
from dotenv import dotenv_values

from app.db_api import DbAPI
from protos import asm_pb2_grpc
from queue_service import pop_message_from_queue
from models import Instance, PoolObservation, Metrics
from services import detener_instancia, crear_instancia, iniciar_instancia, reiniciar_instancia
from utils import InstanceState, Status
from repositories import agregar_instancia

db_api = DbAPI()
config = dotenv_values(".env")
PORT_MONC = config.get('PORT_MONC')


def process_queue():  
    metrics_message = json.loads(pop_message_from_queue())
    if metrics_message.status == Status.HEALTHY.value:
        if pool_in_observation(metrics_message.instance_id):
            prune_pool(instance_url=metrics_message.instance_url)
        # do nothing unless we have an instance in observation
        # if primary and secondary of pool report healthy 3 times and we have other instances stop other instances
    elif metrics_message.status == Status.HEAVYLOAD.value:
        handle_heavyload(metrics_message.instance_id)
        # create instance 
    elif metrics_message.status == Status.CRITICAL.value:
        handle_critical(metrics_message.instance_id)
        # start instance
    else:
        pass    
    with db_api.session_local() as session:
        metrics = Metrics(instance_id = metrics_message.instance_id,
                          cpu_usage = metrics_message.cpu_usage,
                          ram_usage = metrics_message.ram_usage,
                          disk_usage = metrics_message.disk_usage,
                          network_usage = metrics_message.network_usage)
        session.add(metrics)
        session.commit()


def pool_in_observation(instance_url) -> bool:
    with db_api.session_local() as session:
        pool_id = session.query(Instance).filter(instance_endpoint=instance_url).one().pool_id
        return bool(session.query(PoolObservation).filter(pool_id=pool_id).one())


def prune_pool(instance_url):
    with db_api.session_local() as session:
        pool_id = session.query(Instance).filter(instance_endpoint=instance_url).one().pool_id
        pool_instances = session.query(Instance).filter(pool_id=pool_id)
        if len(pool_instances) > 2:
            last_instance = session.query(Instance).filter(pool_id=pool_id).last()
            detener_instancia(last_instance.instance_id)
            last_instance.state = InstanceState.STOPPED
            session.commit()


def handle_heavyload(instance_url):
    with db_api.session_local() as session:
        pool_id = session.query(Instance).filter(instance_endpoint=instance_url).one().pool_id
        new_instance = crear_instancia()
        detener_instancia(instance_id=new_instance.instanceId)
        agregar_instancia(pool_id=pool_id, instance_id=new_instance.instanceId, status=InstanceState.STOPPED)


def handle_critical(instance_url):
    with db_api.session_local() as session:
        pool_id = session.query(Instance).filter(instance_endpoint=instance_url).one().pool_id
        pool_instances = session.query(Instance).filter(pool_id=pool_id)
        for instance in pool_instances:
            if instance.status == InstanceState.STOPPED:
                iniciar_instancia(instance_id=instance.instanceId)
                instance.status = InstanceState.RUNNING
                session.commit()

grpc_config = json.dumps(
    {
        "methodConfig": [
            {
                "name": [{"service": "<package>.<service>"}],
                "retryPolicy": {
                    "maxAttempts": 5,
                    "initialBackoff": "0.1s",
                    "maxBackoff": "10s",
                    "backoffMultiplier": 2,
                    "retryableStatusCodes": ["UNAVAILABLE"],
                },
            }
        ]
    }
)


def send_ping(message) -> str:
    with db_api.session_local() as session:
        active_instances = session.query(Instance).all()
        for instance in active_instances:
            with grpc.insecure_channel(f"{instance.instance_endpoint}:{PORT_MONC}", options=[("grpc.service_config", grpc_config)]) as channel:
                stub = asm_pb2_grpc.MessageStub(channel)
                response = stub.PushMessage(message)
                if not response.success:
                    reiniciar_instancia(instance.instance_id)

    return response.result