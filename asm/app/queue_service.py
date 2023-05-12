import json
from multiprocessing.shared_memory import ShareableList

from app.init_db import db_session
from app.models import Queue, Topic


# Controllador para operaciones de cola, como mvp todas las colas son de profundidad 5 y ordenamiento FIFO


def list_queues():
    queue_list = Queue.query.all()
    queue_name_list = {str(queue.id): queue.name for queue in queue_list}
    return json.dumps(queue_name_list)


def list_topics():
    topic_list = Topic.query.all()
    topic_name_list = {str(topic.id): topic.name for topic in topic_list}
    return json.dumps(topic_name_list)


def create_queue(queue_name):
    # guardando nombre de cola en lista
    # creando cola en memoria
    queue = Queue(name=queue_name)
    db_session.add(queue)
    db_session.commit()
    shared_memory_list = ShareableList([' ' * 1024, ' ' * 1024, ' ' * 1024, ' ' * 1024, ' ' * 1024], name=queue_name)
    return shared_memory_list


def create_topic(topic_name):
    topic = Topic(name=topic_name)
    db_session.add(topic)
    db_session.commit()
    shared_memory_list = ShareableList([' ' * 1024], name=topic_name)
    return shared_memory_list


def push_message_to_queue(queue_name, payload):
    try:
        temp_list = ShareableList(name=queue_name)
        for j in range(5):
            if temp_list[j] == ' ' * 1024:
                temp_list[j] = json.dumps(payload)
                return temp_list
            else:
                continue
        return temp_list
    except FileNotFoundError:
        return f"Queue no encontrada: {queue_name}"


def push_message_to_topic(topic_name, payload):
    try:
        temp_list = ShareableList(name=topic_name)
        temp_list[0] = json.dumps(payload)
        return temp_list
    except FileNotFoundError:
        return f"Topico no encontrada: {topic_name}"


def pop_message_from_queue(queue_name):
    temp_list = ShareableList(name=queue_name)
    for j in range(5):
        if temp_list[j] == ' ' * 1024:
            continue
        else:
            value = temp_list[j]
            temp_list[j] = ' ' * 1024
            return value


def pop_message_from_topic(queue_name):
    temp_list = ShareableList(name=queue_name)
    return temp_list[0]


def delete_queue(queue_name):
    try:
        # remover queue de lista
        queue = Queue.query.filter(Queue.name == queue_name).first()
        db_session.delete(queue)
        db_session.commit()
        # remover queue de memoria
        shared_memory_list = ShareableList(name=queue_name)
        shared_memory_list.shm.unlink()
        return True
    except FileNotFoundError:
        return "Cola no encontrada"

def delete_topic(topic_name):
    try:
        # remover topico de lista
        topic = Topic.query.filter(Topic.name == topic_name).first()
        db_session.delete(topic)
        db_session.commit()
        # remover queue de memoria
        shared_memory_list = ShareableList(name=topic_name)
        shared_memory_list.shm.unlink()
        return True
    except FileNotFoundError:
        return "Topico no encontrado"
