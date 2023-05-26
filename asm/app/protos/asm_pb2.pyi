from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class MetricsRequest(_message.Message):
    __slots__ = ["cpu", "disk", "instance_id", "network", "ram", "status"]
    CPU_FIELD_NUMBER: _ClassVar[int]
    DISK_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    NETWORK_FIELD_NUMBER: _ClassVar[int]
    RAM_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    cpu: float
    disk: float
    instance_id: str
    network: str
    ram: float
    status: str
    def __init__(self, status: _Optional[str] = ..., disk: _Optional[float] = ..., network: _Optional[str] = ..., cpu: _Optional[float] = ..., ram: _Optional[float] = ..., instance_id: _Optional[str] = ...) -> None: ...

class MetricsResponse(_message.Message):
    __slots__ = ["instance_id"]
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    instance_id: str
    def __init__(self, instance_id: _Optional[str] = ...) -> None: ...

class PingRequest(_message.Message):
    __slots__ = ["instance_id"]
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    instance_id: str
    def __init__(self, instance_id: _Optional[str] = ...) -> None: ...

class PingResponse(_message.Message):
    __slots__ = ["success"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
