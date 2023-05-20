from flask import Response, request
from sqlalchemy.orm import sessionmaker
from app.protos import mom_pb2
from models import Pool, Instance
from services import crear_instancia
from boto3.ec2 import instance

# Manda mensaje para que la cola se cree
session = sessionmaker()

def crear_pool(pool_name) -> Response:
    # crear pool en bd
    pool = Pool(name=pool_name)
    session.add(pool)
    session.commit()
    #crear instancias iniciales
    instance_1 = crear_instancia()
    record_instancia_1 = Instance(pool_id=pool.id, instance_id=instance_1.instanceId)
    
    # agregar instancias a bd

    


def eliminar_pool() -> Response:
    pass



