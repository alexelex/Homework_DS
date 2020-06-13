from django_grpc_framework.services import Service
from django_grpc_framework import proto_serializers
from .models import UserInfo, Users
from genrpc import config_pb2, config_pb2_grpc
import datetime

def handlers(server):
    config_pb2_grpc.add_AuthServicer_to_server(Auth.as_servicer(), server)

class Auth(Service):
    def Verification(self, request, context):
        info = UserInfo()
        try:
            note = Users.objects.filter(
                access_token=request.token,
            )

            if not note.exists():
                raise Exception
            if note.count() > 1:
                raise Exception
            note = note[0]
            if not note.activated:
                raise Exception
            if note.time_modified.replace(tzinfo=None) <= datetime.datetime.now() - datetime.timedelta(hours=2):
                raise Exception
            info.verify_status = True
            info.email = note.email
            info.role = note.role
            if note.email == "admin":
                info.role = Users.MODERATOR
        except Exception:
            pass
        return UserInfoSerializer(info).message

class UserInfoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = UserInfo
        proto_class = config_pb2.UserInfo
        fields = ['verify_status', 'email', 'role']
