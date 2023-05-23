from flask import Response
from app.models import Pool, Instance
from app.services import crear_instancia, eliminar_instancia
from app.repositories import agregar_pool
from app.db_api import DbAPI

db_api = DbAPI()


def crear_pool(pool_name) -> Response:
    with db_api.session_local as session:
        # crear pool en bd
        pool = agregar_pool(pool_name)
        # crear instancias iniciales
        instance_1 = crear_instancia()
        record_instancia_1 = Instance(pool_id=pool.id, instance_id=instance_1.instanceId)
        instance_2 = crear_instancia()
        record_instancia_2 = Instance(pool_id=pool.id, instance_id=instance_2.instanceId)
        # agregar instancias a bd
        session.add(record_instancia_1)
        session.add(record_instancia_2)
        session.commit()

    return Response(status=200, response=f"pool creado con 2 nodos, {instance_1.instanceId} y {instance_2.instanceId}")


def eliminar_pool(pool_name) -> Response:
    with db_api.session_local as session:
        pool = session.query(Pool).filter(pool_name=pool_name).one()
        instances = session.query(Instance).filter(pool_id=pool.id)
        for instance in instances:
            eliminar_instancia(instance_id=instance.id)
    return Response(status=200, response="pool eliminado")

