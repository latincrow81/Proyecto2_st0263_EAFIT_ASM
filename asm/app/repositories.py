from app.models import Pool, Instance, PoolObservation
from app.db_api import DbAPI

db_api = DbAPI()


def buscar_pool(pool_name) -> Pool:
    with db_api.session_local() as session:
        pool = session.query(Pool).filter(pool_name=pool_name).one()
    return pool


def agregar_pool(pool_name) -> Pool:
    with db_api.session_local(expire_on_commit=False) as session:
        pool = Pool(pool_name=pool_name)
        session.add(pool)
        session.commit()

    return pool


def remover_pool(pool_name) -> None:
    with db_api.session_local() as session:
        session.query(Pool).filter(pool_name=pool_name).delete()


def agregar_instancia(pool_id, instance_id):
    with db_api.session_local(expire_on_commit=False) as session:
        instance = Instance(pool_id=pool_id, Instance_id=instance_id)
        session.add(instance)
        session.commit()

    return instance


def instancias_por_pool_id(pool_id):
    with db_api.session_local() as session:
        instancias = session.query(Instance).filter(pool_id=pool_id)
    return instancias


def remover_instancia(instance_id):
    with db_api.session_local() as session:
        session.query(Instance).filter(instance_id=instance_id).delete()


def agregar_pool_a_observacion(pool_id):
    with db_api.session_local(expire_on_commit=False) as session:
        pool_observation = PoolObservation(pool_id=pool_id)
        session.add(pool_observation)
        session.commit()


def remover_pool_de_observacion(pool_id):
    with db_api.session_local() as session:
        session.query(PoolObservation).filter(pool_id=pool_id).delete()