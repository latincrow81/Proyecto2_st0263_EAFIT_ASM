import json
import grpc
from dotenv import dotenv_values
from boto3 import ec2
from protos import asm_pb2_grpc

config = dotenv_values(".env")

HOST_GRPC = config.get('HOST_MOM')
PORT_GRPC = config.get('PORT_MOM')


def send_ping(message) -> str:
    with grpc.insecure_channel(f"{HOST_GRPC}:{PORT_GRPC}") as channel:
        stub = asm_pb2_grpc.MessageStub(channel)
        response = stub.PushMessage(message)

    return response.result

def crear_instancia():
    instance = ec2.create_instances(
    InstanceType='t2.micro',
    Monitoring={
        'Enabled': True
    },
    SecurityGroupIds=[
        'sg-0e5842b06c8ed87f8',
    ],
    EbsOptimized=True,
    InstanceInitiatedShutdownBehavior='stop',
    
    LaunchTemplate={
        'LaunchTemplateId': 'lt-0e7478d2842766243',
        'LaunchTemplateName': 'SeedASG',
        'Version': '1'
    }
)

return instance
