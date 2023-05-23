from sqlalchemy.orm import sessionmaker
from app.models import Pool, Instance, PoolObservation

session = sessionmaker()

def buscar_pool(pool_name) -> Pool:
    pool = session.query(Pool).filter(pool_name=pool_name).one()
    return pool

def agregar_pool(pool_name) -> Pool:
    pool = Pool(name=pool_name)
    session.add(pool)
    session.commit()

    return pool

def remover_pool(pool_name) -> None:
    session.query(Pool).filter(pool_name=pool_name).delete()

def agregar_instancia(pool_id, instance_id):
    instance = Instance(pool_id=pool_id, Instance_id=instance_id)
    session.add(instance)
    session.commit()

    return instance

def remover_instancia(instance_id):
    session.query(Instance).filter(instance_id=instance_id).delete()

def agregar_pool_a_observacion(pool_id):
    pool_observation = PoolObservation(pool_id=pool_id)
    session.add(pool_observation)
    session.commit()

def remover_pool_de_observacion(pool_id):
    session.query(PoolObservation).filter(pool_id=pool_id).delete()