from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from erp_system.utils.batch_destroy import BatchDestroy
from erp_systems.models import PermissionModel
from erp_systems.serializer.permission_serializer import PermissionSerializer


class PermissionViewSet(viewsets.ModelViewSet, BatchDestroy):
    """
    list:
    权限--获取列表

    获取权限列表，status：200（成功），return：权限列表

    create:
    权限--新增

    权限新增，status：201（成功），return：新增权限信息

    read:
    权限--获取某个权限的详情

    获取某个权限的详情，status：200（成功），return：某个权限的详情
    update:
    权限--修改

    权限修改，status：200（成功），return：修改后的权限信息

    partial_update:
    权限--部分修改

    部分权限修改，status：200（成功），return：修改后的权限信息

    delete:
    权限--删除

    权限删除，status：204（成功），return：空

    batch_destroy:
    权限--批量删除

    权限批量删除，status：204（成功），return：空

    get_menu_id_permission:
    权限--根据菜单的id查询当前菜单或者接口的所有权限

    根据菜单的id查询当前菜单或者接口的所有权限，status：200（成功），return：当前菜单或者接口的所有权限
    """
    queryset = PermissionModel.objects.all()
    serializer_class = PermissionSerializer

    # 根据菜单的id查询当前菜单或者接口的所有权限
    @swagger_auto_schema(methods=['get'], manual_parameters=[
        openapi.Parameter(name='menu_id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='菜单id')])
    @action(methods=['get'], detail=False)
    def get_menu_id_permission(self, request, *args, **kwargs):
        # 获取传过来的menu_id
        menu_id = request.query_params.get('menu_id')
        if not menu_id:
            return Response(data={'detail': "参数错误，menu_id为必传参数"}, status=status.HTTP_400_BAD_REQUEST)
        # 根据menu_id查询权限
        permission = PermissionModel.objects.filter(menu_id=menu_id).all()
        # 序列化
        ser = PermissionSerializer(instance=permission, many=True)
        return Response(ser.data)
