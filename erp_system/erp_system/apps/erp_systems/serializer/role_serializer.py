from rest_framework import serializers

from erp_systems.models import RoleModel
from erp_systems.serializer.permission_serializer import PermissionSerializer


class RoleSerializer(serializers.ModelSerializer):
    """
    角色的序列化器，具有常规角色的增删改查功能
    """
    # 需要查询角色的时候，将角色所拥有的权限也查出来，需要嵌套序列化器
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = RoleModel
        fields = '__all__'


class BatchSetPermissionSerializer(serializers.ModelSerializer):
    """
    批量设置角色的权限的序列化器
    """

    class Meta:
        model = RoleModel
        fields = ['id', 'permissions']


class SetPermissionSerializer(serializers.Serializer):
    """
    单一设置角色权限的增加
    """
    # 角色id
    role_id = serializers.IntegerField(write_only=True, required=True)
    # 权限id
    permission_id = serializers.IntegerField(write_only=True, required=True)
    # 是否添加权限
    is_create = serializers.BooleanField(write_only=True, required=True)
