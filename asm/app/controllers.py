from flask import Response, request

from app.protos import mom_pb2
from .services import send_message, get_message, send_message_topic, get_message_topic


# Manda mensaje para que la cola se cree


def list_instances() -> Response:
    pass

