import grpc
import json
from concurrent import futures
from enum import Enum
from services import reiniciar_instancia
from dotenv import dotenv_values
from sqlalchemy.orm import sessionmaker
from app.protos import asm_pb2_grpc
from models import Instance

session = sessionmaker()

config = dotenv_values(".env")

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

PORT_MONC = config.get('PORT_MONC')
PORT_ASM = config.get('PORT_ASM')



class Handler(asm_pb2_grpc.MonitorServiceServicer):

    def GetMetrics(self, request, context):
       pass

def send_ping(message) -> str:
    active_instances = session.query(Instance).all()
    for instance in active_instances:
        with grpc.insecure_channel(f"{instance.instance_endpoint}:{PORT_ASM}", options=[("grpc.service_config", grpc_config)]) as channel:
            stub = asm_pb2_grpc.MessageStub(channel)
            response = stub.PushMessage(message)
            if not response.success:
                reiniciar_instancia(instance.instance_id)


    return response.result

def run_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    asm_pb2_grpc.add_MonitorServiceServicer_to_server(Handler(), server)
    server.add_insecure_port('[::]:' + PORT_ASM)
    server.start()
    print(f'MonitorS en ejecución en el puerto {PORT_ASM}...')
    server.wait_for_termination()
