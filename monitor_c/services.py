import grpc
import socket
import psutil
from enum import Enum
from dotenv import dotenv_values
from protos import asm_pb2_grpc, asm_pb2

config = dotenv_values(".env")

HOST_ASM = config.get('HOST_ASM')
PORT_ASM = config.get('PORT_ASM')


class Handler(asm_pb2_grpc.MonitorServiceServicer):
    def Ping(self, request, context):
        return asm_pb2.PingResponse(success=True)


def send_status(message) -> str:
    print(message)
    with grpc.insecure_channel(f"{HOST_ASM}:{PORT_ASM}") as channel:
        stub = asm_pb2_grpc.MonitorServiceStub(channel)
        response = stub.GetMetrics(message)
        print(message)
    return response.result


def get_system_status():
    status = Status.HEALTHY.value
    cpu_state = psutil.getloadavg()[1]
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/')
    network = psutil.net_io_counters(pernic=True)
    #network_usage = f"{network.get('eth0').bytes_sent}/{network.get('eth0').bytes_recv}"
    network_usage = ""
    instance_id = socket.gethostname()
    
    if cpu_state > 0.1:
        status = Status.BASELOAD.value
    if cpu_state > 0.4:
        status = Status.HEAVYLOAD.value
    if cpu_state > 0.8:
        status = Status.CRITICAL.value
    if ram_usage > 70:
        status = Status.HEAVYLOAD.value
    if ram_usage > 90:
        status = Status.CRITICAL.value
    
    response = asm_pb2.MetricsRequest(status=status,
                                      disk=disk_usage.percent,
                                      network=network_usage,
                                      cpu=cpu_state,
                                      ram=ram_usage,
                                      instance_id=instance_id)
    send_status(response)


class Status(Enum):
    HEALTHY = 'healthy'
    BASELOAD = 'baseload'
    HEAVYLOAD = 'heavyload'
    CRITICAL = 'critical'

get_system_status()
