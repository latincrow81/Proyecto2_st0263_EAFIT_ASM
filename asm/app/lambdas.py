from sqlalchemy.orm import sessionmaker
from queue_service import pop_message_from_queue
from models import Instance, PoolObservation
from services import detener_instancia, crear_instancia, iniciar_instancia
from utils import InstanceState, Status
from repositories import agregar_instancia

session = sessionmaker()

def process_queue():  
    metrics_message = pop_message_from_queue()
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



def pool_in_observation(instance_url) -> bool:
    pool_id = session.query(Instance).filter(instance_endpoint=instance_url).one().pool_id
    return bool(session.query(PoolObservation).filter(pool_id=pool_id).one())

def prune_pool(instance_url):
    pool_id = session.query(Instance).filter(instance_endpoint=instance_url).one().pool_id
    pool_instances = session.query(Instance).filter(pool_id=pool_id)
    if len(pool_instances) > 2:
        last_instance = session.query(Instance).filter(pool_id=pool_id).last()
        detener_instancia(last_instance.instance_id)
        last_instance.state = InstanceState.STOPPED
        session.commit()

def handle_heavyload(instance_url):
    pool_id = session.query(Instance).filter(instance_endpoint=instance_url).one().pool_id
    new_instance = crear_instancia()
    detener_instancia(instance_id=new_instance.instanceId)
    agregar_instancia(pool_id=pool_id, instance_id=new_instance.instanceId, status=InstanceState.STOPPED)


def handle_critical(instance_url):
    pool_id = session.query(Instance).filter(instance_endpoint=instance_url).one().pool_id
    pool_instances = session.query(Instance).filter(pool_id=pool_id)
    for instance in pool_instances:
        if instance.status == InstanceState.STOPPED:
            iniciar_instancia(instance_id=instance.instanceId)
            instance.status = InstanceState.RUNNING
            session.commit()