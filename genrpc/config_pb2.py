# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: genrpc/config.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='genrpc/config.proto',
  package='authorization',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\x13genrpc/config.proto\x12\rauthorization\"\x16\n\x05Token\x12\r\n\x05token\x18\x01 \x01(\t\">\n\x08UserInfo\x12\x15\n\rverify_status\x18\x01 \x01(\x08\x12\r\n\x05\x65mail\x18\x02 \x01(\t\x12\x0c\n\x04role\x18\x03 \x01(\t2E\n\x04\x41uth\x12=\n\x0cVerification\x12\x14.authorization.Token\x1a\x17.authorization.UserInfob\x06proto3'
)




_TOKEN = _descriptor.Descriptor(
  name='Token',
  full_name='authorization.Token',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='token', full_name='authorization.Token.token', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=38,
  serialized_end=60,
)


_USERINFO = _descriptor.Descriptor(
  name='UserInfo',
  full_name='authorization.UserInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='verify_status', full_name='authorization.UserInfo.verify_status', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='email', full_name='authorization.UserInfo.email', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='role', full_name='authorization.UserInfo.role', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=62,
  serialized_end=124,
)

DESCRIPTOR.message_types_by_name['Token'] = _TOKEN
DESCRIPTOR.message_types_by_name['UserInfo'] = _USERINFO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Token = _reflection.GeneratedProtocolMessageType('Token', (_message.Message,), {
  'DESCRIPTOR' : _TOKEN,
  '__module__' : 'genrpc.config_pb2'
  # @@protoc_insertion_point(class_scope:authorization.Token)
  })
_sym_db.RegisterMessage(Token)

UserInfo = _reflection.GeneratedProtocolMessageType('UserInfo', (_message.Message,), {
  'DESCRIPTOR' : _USERINFO,
  '__module__' : 'genrpc.config_pb2'
  # @@protoc_insertion_point(class_scope:authorization.UserInfo)
  })
_sym_db.RegisterMessage(UserInfo)



_AUTH = _descriptor.ServiceDescriptor(
  name='Auth',
  full_name='authorization.Auth',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=126,
  serialized_end=195,
  methods=[
  _descriptor.MethodDescriptor(
    name='Verification',
    full_name='authorization.Auth.Verification',
    index=0,
    containing_service=None,
    input_type=_TOKEN,
    output_type=_USERINFO,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_AUTH)

DESCRIPTOR.services_by_name['Auth'] = _AUTH

# @@protoc_insertion_point(module_scope)