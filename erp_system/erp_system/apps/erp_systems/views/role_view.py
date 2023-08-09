from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from erp_system.utils.batch_destroy import BatchDestroy
from erp_systems.models import RoleModel, PermissionModel
from erp_systems.serializer.role_serializer import BatchSetPermissionSerializer, RoleSerializer, SetPermissionSerializer


class RoleViewSet(viewsets.ModelViewSet, BatchDestroy):
    """
    create:
    角色--新增

    角色新增，status：201（成功），return：新增角色信息

    destroy:
    角色--删除

    角色删除，status：204（成功），return：空

    batch_destroy:
    角色--批量删除

    角色批量删除，status：204（成功），return：空

    update:
    角色--修改

    角色修改，status：200（成功），return：修改后的角色信息

    partial_update:
    角色--部分修改,批量授权

    部分角色授权，status：200（成功），return：授权后的角色信息

    list:
    角色--获取列表

    获取角色列表，status：200（成功），return：角色列表

    set_permission:
    角色--单一设置角色权限

    单一设置角色权限，status：200（成功），return：修改后的角色信息

    read:
    角色--获取某个角色的详情

    获取某个角色的详情，status：200（成功），return：某个角色的详情

    batchdestroy:
    角色--批量删除

    角色批量删除，status：204（成功），return：空


    """
    queryset = RoleModel.objects.all()

    # 序列化器类
    def get_serializer_class(self):
        if self.action == 'partial_update':
            return BatchSetPermissionSerializer
        elif self.action == 'set_permission':
            return SetPermissionSerializer
        else:
            return RoleSerializer

    # 单一设置角色权限
    @action(methods=['post'], detail=False)
    def set_permission(self, request, *args, **kwargs):
        ser = SetPermissionSerializer(data=request.data)
        if ser.is_valid():  # 参数验证通过
            # 获取角色id
            role_id = RoleModel.objects.get(id=ser.validated_data['role_id'])
            # 获取权限的id
            permission_id = PermissionModel.objects.get(id=ser.validated_data['permission_id'])
            # 判断是否添加权限
            is_create = ser.validated_data['is_create']
            if is_create:
                # 添加权限
                role_id.permissions.add(permission_id)
                return Response({'msg': '添加权限成功', 'status': 200})
            else:
                role_id.permissions.remove(permission_id)
                return Response({'msg': '删除权限成功', 'status': 200})

            role_result = RoleSerializer(instance=role_id)
            return Response(data=role_result.data)

    def destroy(self, request, *args, **kwargs):
        # 重写删除方法，不能删除admin这个角色
        if self.get_object().name == 'admin':
            return Response({'msg': 'admin角色不能删除', 'status': 400})
        return super().destroy(request, *args, **kwargs)

    @action(methods=['delete'], detail=False)
    def batchdestroy(self, request, *args, **kwargs):
        # 重写批量删除方法，不能删除admin这个角色
        del_ids = request.data.get('ids')
        try:
            if isinstance(del_ids,list):
                admin = RoleModel.objects.get(name='admin')
                if admin.id in del_ids:
                    return Response({'msg': 'admin角色不能删除', 'status': 400})
        except RoleModel.DoesNotExist as ex:
            pass

        return super().batchdestroy(request, *args, **kwargs)
