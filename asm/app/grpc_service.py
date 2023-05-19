import grpc
from concurrent import futures
from enum import Enum

from dotenv import dotenv_values

from app.protos import asm_pb2_grpc, asm_pb2

config = dotenv_values(".env")

SERVER_ADDRESS = config.get('HOST_MOM')
GRPC_PORT = config.get('PORT_MOM')

class Handler(asm_pb2_grpc.MonitorServiceServicer):

    def GetMetrics(self, request, context):
        if request.status == Status.HEALTHY.value:
           pass
           # do nothing unless we have an instance in observation
           # if primary and secondary of pool report healthy 3 times and we have other instances stop other instances 
        elif request.op == Status.BASELOAD.value:
           pass
           # do nothing
        elif request.op == Status.HEAVYLOAD.value:
           pass
           # create instance 
        elif request.op == Status.CRITICAL.value:
           pass
           # start instance
        else:
            pass

   

class Status(Enum):
    HEALTHY = 'healthy'
    BASELOAD = 'baseload'
    HEAVYLOAD = 'heavyload'
    CRITICAL = 'critical'
