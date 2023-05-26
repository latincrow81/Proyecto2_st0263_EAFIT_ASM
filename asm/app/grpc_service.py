import grpc
from concurrent import futures

from app.queue_service import push_message_to_queue
from protos import asm_pb2
from dotenv import dotenv_values
from sqlalchemy.orm import sessionmaker
from app.protos import asm_pb2_grpc

session = sessionmaker()

config = dotenv_values(".env")

PORT_MONC = config.get('PORT_MONC')
PORT_ASM = config.get('PORT_ASM')


class Handler(asm_pb2_grpc.MonitorServiceServicer):
    def get_metrics(self, request):
        push_message_to_queue(request)
        return asm_pb2.MetricsResponse(instance_id=request.instance_id)


def run_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    asm_pb2_grpc.add_MonitorServiceServicer_to_server(Handler(), server)
    server.add_insecure_port('[::]:' + PORT_ASM)
    server.start()
    print(f'MonitorS en ejecución en el puerto {PORT_ASM}...')
    server.wait_for_termination()
