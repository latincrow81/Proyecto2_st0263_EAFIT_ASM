# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: asm.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\tasm.proto\x12\x03\x61sm\"\"\n\x0bPingRequest\x12\x13\n\x0binstance_id\x18\x01 \x01(\t\"\x1f\n\x0cPingResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"&\n\x0fMetricsResponse\x12\x13\n\x0binstance_id\x18\x01 \x01(\t\"n\n\x0eMetricsRequest\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x0c\n\x04\x64isk\x18\x02 \x01(\x05\x12\x0f\n\x07network\x18\x03 \x01(\x05\x12\x0b\n\x03\x63pu\x18\x04 \x01(\x05\x12\x0b\n\x03ram\x18\x05 \x01(\x05\x12\x13\n\x0binstance_id\x18\x06 \x01(\t2z\n\x0eMonitorService\x12-\n\x04Ping\x12\x10.asm.PingRequest\x1a\x11.asm.PingResponse\"\x00\x12\x39\n\nGetMetrics\x12\x13.asm.MetricsRequest\x1a\x14.asm.MetricsResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'asm_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _PINGREQUEST._serialized_start=18
  _PINGREQUEST._serialized_end=52
  _PINGRESPONSE._serialized_start=54
  _PINGRESPONSE._serialized_end=85
  _METRICSRESPONSE._serialized_start=87
  _METRICSRESPONSE._serialized_end=125
  _METRICSREQUEST._serialized_start=127
  _METRICSREQUEST._serialized_end=237
  _MONITORSERVICE._serialized_start=239
  _MONITORSERVICE._serialized_end=361
# @@protoc_insertion_point(module_scope)
