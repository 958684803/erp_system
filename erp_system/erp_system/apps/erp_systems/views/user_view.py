from rest_framework import viewsets
from rest_framework.generics import CreateAPIView

from erp_systems.models import UserModel
from erp_systems.serializer.user_serializer import RegisterUserSerializer


class RegisterUserView(CreateAPIView):
    """
	    用户注册的视图类
    """
    queryset = UserModel.objects.all()
    serializer_class = RegisterUserSerializer
