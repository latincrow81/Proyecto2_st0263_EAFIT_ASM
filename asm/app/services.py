import json

import grpc

from dotenv import dotenv_values

from app.protos import mom_pb2_grpc

config = dotenv_values(".env")

HOST_GRPC = config.get('HOST_MOM')
PORT_GRPC = config.get('PORT_MOM')


def send_message(message) -> str:
    with grpc.insecure_channel(f"{HOST_GRPC}:{PORT_GRPC}") as channel:
        stub = mom_pb2_grpc.MessageQueueStub(channel)
        response = stub.PushMessage(message)

    return response.result


def get_message(message) -> str:
    with grpc.insecure_channel(f"{HOST_GRPC}:{PORT_GRPC}") as channel:
        stub = mom_pb2_grpc.MessageQueueStub(channel)
        response = stub.PullMessage(message)

    return response.payload


def get_message_topic(message) -> str:
    with grpc.insecure_channel(f"{HOST_GRPC}:{PORT_GRPC}") as channel:
        stub = mom_pb2_grpc.MessageQueueStub(channel)
        response = stub.PullTopic(message)

    return response.result


def send_message_topic(message) -> str:
    with grpc.insecure_channel(f"{HOST_GRPC}:{PORT_GRPC}") as channel:
        stub = mom_pb2_grpc.MessageQueueStub(channel)
        response = stub.PushTopic(message)

    return response.result
