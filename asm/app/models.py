from .auth.models import User, AnonymousUser
from .. import db
from datetime import datetime

class Pool(db.Model):
    __tablename__ = 'pool'
    id = db.Column(db.Integer, primary_key=True)
    pool_name = db.Column(db.String(60), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

class Instance(db.Model):
    __tablename__ = 'instance'
    id = db.Column(db.Integer, primary_key=True)
    instance_id = db.Column(db.String(60), unique=True, nullable=False)
    pool_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

class Metrics(db.Model):
    __tablename__ = 'metric'
    id = db.Column(db.Integer, primary_key=True)
    instance_id = db.Column(db.String(60), unique=True, nullable=False)
    cpu_usage = db.Column(db.Integer, nullable=False)
    ram_usage = db.Column(db.Integer, nullable=False)
    disk_usage = db.Column(db.Integer, nullable=False)
    network_usage = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
