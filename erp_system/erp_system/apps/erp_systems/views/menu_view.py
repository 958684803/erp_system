import logging

from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from erp_systems.models import MenuModel
from erp_systems.serializer.menu_serializer import MenuSerializer

logger = logging.getLogger('erp')


# Create your views here.

# 创建菜单的视图类
class MenuView(viewsets.ModelViewSet):
    """
    list:
    菜单--获取列表

    获取菜单列表，status：200（成功），return：菜单列表

    create:
    菜单--新增

    菜单新增，status：201（成功），return：新增菜单信息

    batch_destroy:
    菜单--批量删除

    菜单批量删除，status：204（成功），return：空

    read:
    菜单--获取某个菜单的详情

    获取某个菜单的详情，status：200（成功），return：某个菜单的详情

    update:
    菜单--修改

    菜单修改，status：200（成功），return：修改后的菜单信息

    partial_update:
    菜单--部分修改

    部分菜单修改，status：200（成功），return：修改后的菜单信息

    delete:
    菜单--删除

    菜单删除，status：204（成功），return：空
    """
    permission_classes = [IsAuthenticated, ]
    queryset = MenuModel.objects.filter(delete_flag='0').all()
    serializer_class = MenuSerializer

    def get_queryset(self):

        """
        # 1. 查询所有功能菜单
        # 2. 查询某个父菜单下面所有的子菜单
        """
        query_param = self.request.query_params.get('pid', None)
        if query_param:
            pid = int(query_param)
            if pid == 0:
                return MenuModel.objects.filter(delete_flag='0', parent__isnull=True).all()
            else:
                return MenuModel.objects.filter(delete_flag='0', parent_id=pid).all()
        else:
            return MenuModel.objects.filter(delete_flag='0').all()

    def destroy(self, request, *args, **kwargs):


        instance = self.get_object()
        instance.delete_flag = '1'
        instance.save()
        # 可能该菜单下面还有子菜单，也需要删除
        MenuModel.objects.filter(parent_id=instance.id).update(delete_flag='1')
        return Response(status=status.HTTP_204_NO_CONTENT)

    del_ids = openapi.Schema(type=openapi.TYPE_OBJECT,required=['ids'],properties={
        'ids': openapi.Schema(type=openapi.TYPE_ARRAY,items=openapi.Schema(type=openapi.TYPE_INTEGER),description='需要删除的菜单id列表')
    })

    @swagger_auto_schema(methods=['delete'], request_body=del_ids)
    @action(methods=['delete'], detail=False)
    def batch_destroy(self, request, *args, **kwargs):
        ids = request.data.get('ids', None)
        if not ids:
            return Response(data={'detail': '参数错误，ids为必传参数'}, status=status.HTTP_400_BAD_REQUEST)
        elif not isinstance(ids, list):
            return Response(data={'detail': '参数错误，ids必须为列表'}, status=status.HTTP_400_BAD_REQUEST)

        # 先删除传递过来的功能菜单
        MenuModel.objects.filter(id__in=ids).update(delete_flag='1')
        # 再删除传递过来的功能菜单下面的子菜单
        for id in ids:
            MenuModel.objects.filter(parent_id=id).update(delete_flag='1')
        return Response(status=status.HTTP_204_NO_CONTENT)
