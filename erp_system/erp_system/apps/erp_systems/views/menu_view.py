from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from erp_systems.models import MenuModel
from erp_systems.serializer.menu_serializer import MenuSerializer


# Create your views here.

# 创建菜单的视图类
class MenuView(viewsets.ModelViewSet):
    """
    新增功能菜单的模型类

    1。新增菜单
    2. 查询单个功能菜单
    3. 查询所有功能菜单
    4. 查询某个父菜单下面所有的子菜单
    5. 修改功能菜单
    6. 删除某一个功能菜单
    7. 查询所有的顶级菜单列表
    8. 批量删除
    """
    queryset = MenuModel.objects.filter(delete_flag='o').all()
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
        """
            # 6. 删除某一个功能菜单
        """

        instance = self.get_object()
        instance.delete_flag = '1'
        instance.save()
        # 可能该菜单下面还有子菜单，也需要删除
        MenuModel.objects.filter(parent_id=instance.id).update(delete_flag='1')
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['delete'], detail=False)
    def destroy_all(self, request, *args, **kwargs):
        ids = request.data.get('ids', None)
        if not ids:
            return Response(data={'detail':'参数错误，ids为必传参数'},status=status.HTTP_400_BAD_REQUEST)
        elif not isinstance(ids,list):
            return Response(data={'detail':'参数错误，ids必须为列表'},status=status.HTTP_400_BAD_REQUEST)

        # 先删除传递过来的功能菜单
        MenuModel.objects.filter(id__in=ids).update(delete_flag='1')
        # 再删除传递过来的功能菜单下面的子菜单
        for id in ids:
            MenuModel.objects.filter(parent_id=id).update(delete_flag='1')
        return Response(status=status.HTTP_204_NO_CONTENT)

