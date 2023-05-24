import json
from multiprocessing.shared_memory import ShareableList
from typing import Optional, Union

# Controllador para operaciones de cola, se usara una cola de 20 posiciones
STATS_QUEUE_NAME = "asm_stats"


def init_stats_queue():
    # guardando nombre de cola en lista
    # creando cola en memoria
    shared_memory_list = ShareableList([' ' * 1024, ' ' * 1024, ' ' * 1024, ' ' * 1024, ' ' * 1024,
                                        ' ' * 1024, ' ' * 1024, ' ' * 1024, ' ' * 1024, ' ' * 1024,
                                        ' ' * 1024, ' ' * 1024, ' ' * 1024, ' ' * 1024, ' ' * 1024,
                                        ' ' * 1024, ' ' * 1024, ' ' * 1024, ' ' * 1024, ' ' * 1024], name=STATS_QUEUE_NAME)
    return shared_memory_list


def push_message_to_queue(payload) -> Union[ShareableList, str]:
    try:
        temp_list = ShareableList(name=STATS_QUEUE_NAME)
        for j in range(20):
            if temp_list[j] == ' ' * 1024:
                temp_list[j] = json.dumps(payload)
                return temp_list
            else:
                continue
        return temp_list
    except FileNotFoundError:
        return f"Queue no encontrada: {STATS_QUEUE_NAME}"


def pop_message_from_queue() -> str:
    temp_list = ShareableList(name=STATS_QUEUE_NAME)
    for j in range(20, 0):
        if temp_list[j] == ' ' * 1024:
            continue
        else:
            value = temp_list[j]
            temp_list[j] = ' ' * 1024
            return value
