from rest_framework import viewsets, mixins
from rest_framework.generics import CreateAPIView, UpdateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from erp_system.utils.batch_destroy import BatchDestroy
from erp_system.utils.global_page import GlobalPagination
from erp_systems.models import UserModel
from erp_systems.serializer.user_serializer import RegisterUserSerializer, UserUpdateDeleteSerializer, \
    UserGetSerializer, UpdatePassWordSerializer


class RegisterUserView(CreateAPIView):
    """
	    用户注册的视图类
    """
    queryset = UserModel.objects.all()
    serializer_class = RegisterUserSerializer


class UserView(mixins.UpdateModelMixin,
               mixins.RetrieveModelMixin,
               mixins.DestroyModelMixin,
               mixins.ListModelMixin,
               BatchDestroy,
               GenericViewSet):
    """
    update:
    用户--修改

    用户修改，status：200（成功），return：修改后的用户信息

    destroy:
    用户--删除

    用户删除，status：204（成功），return：空

    batchdestroy:
    用户--批量删除

    用户批量删除，status：204（成功），return：空

    retrieve:
    用户--获取某个用户的详情

    获取某个用户的详情，status：200（成功），return：某个用户的详情

    list:
    用户--获取列表

    获取用户列表，status：200（成功），return：用户列表

    partial_update:
    用户--部分修改

    部分用户修改，status：200（成功），return：修改后的用户信息

    """
    queryset = UserModel.objects.all()
    pagination_class = GlobalPagination

    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'partial_update' or self.action == 'delete':
            return UserUpdateDeleteSerializer
        else:
            return UserGetSerializer


class UpdatePassWordView(mixins.UpdateModelMixin, GenericAPIView):
    """
    patch:
    用户--修改密码

    修改密码，status：200（成功），return：修改后的用户信息
    """
    queryset = UserModel.objects.all()
    serializer_class = UpdatePassWordSerializer

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
