import grpc
from concurrent import futures
from dotenv import dotenv_values
from protos import asm_pb2_grpc
from services import Handler


config = dotenv_values(".env")


GRPC_PORT = config.get('PORT_MONC')


def run_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    asm_pb2_grpc.add_MonitorServiceServicer_to_server(Handler(), server)
    server.add_insecure_port('[::]:' + GRPC_PORT)
    server.start()
    print(f'MonitorC en ejecución en el puerto {GRPC_PORT}...')
    server.wait_for_termination()


run_server()
