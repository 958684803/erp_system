from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from erp_systems.models import PermissionModel
from erp_systems.serializer.permission_serializer import PermissionSerializer


class PermissionViewSet(viewsets.ModelViewSet):
    """
    权限模型的视图类
    """
    queryset = PermissionModel.objects.all()
    serializer_class = PermissionSerializer

    # 根据菜单的id查询当前菜单或者接口的所有权限
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
