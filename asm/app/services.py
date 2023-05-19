import json

import grpc

from dotenv import dotenv_values

from protos import asm_pb2_grpc

config = dotenv_values(".env")

HOST_GRPC = config.get('HOST_MOM')
PORT_GRPC = config.get('PORT_MOM')


def send_ping(message) -> str:
    with grpc.insecure_channel(f"{HOST_GRPC}:{PORT_GRPC}") as channel:
        stub = asm_pb2_grpc.MessageStub(channel)
        response = stub.PushMessage(message)

    return response.result
