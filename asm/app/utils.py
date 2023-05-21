from . import db
from enum import Enum


class ModelMixin(object):

    def save(self):
        # Save this model to the database.
        db.session.add(self)
        db.session.commit()
        return self


# Add your own utility classes and functions here.
class InstanceState(Enum):
    RUNNING = 'running'
    STOPPED = 'stopped'


class Status(Enum):
    HEALTHY = 'healthy'
    BASELOAD = 'baseload'
    HEAVYLOAD = 'heavyload'
    CRITICAL = 'critical'