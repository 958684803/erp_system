import re

from rest_framework import serializers, mixins

from erp_systems.models import UserModel
from erp_systems.serializer.dept_serializer import DeptSerializer
from erp_systems.serializer.role_serializer import RoleSerializer


class RegisterUserSerializer(serializers.ModelSerializer):
    """
    用户的序列化器
    """

    class Meta:
        model = UserModel
        fields = ['id', 'username', 'password', 'phone', 'real_name']

        extra_kwargs = {
            'username': {
                'min_length': 2,
                'max_length': 20,
            },
            'password': {
                'min_length': 6,
                'max_length': 20,
                'write_only': True,
            }
        }

    # 验证手机号(格式: validate_字段名)
    def validate_phone(self, phone):
        if not phone:
            return phone
        if not re.match(r'^1[35789]\d{9}$', phone):
            raise serializers.ValidationError('手机号格式错误')
        return phone

    # 重写create方法，因为：密码需要加密，而且需要保存用户的真实姓名
    def create(self, validated_data):
        return UserModel.objects.create_user(**validated_data)


class UserUpdateDeleteSerializer(serializers.ModelSerializer):
    """
    只进行用户的修改和删除的序列化器
    """
    class Meta:
        model = UserModel
        fields = ['id', 'phone', 'real_name', 'roles', 'dept']


class UserGetSerializer(serializers.ModelSerializer):
    """
    用查询用户和用户详情的序列化器
    """
    roles = RoleSerializer(many=True, read_only=True)
    dept = DeptSerializer(many=False, read_only=True)

    class Meta:
        model = UserModel
        fields = ['id', 'username', 'phone', 'real_name', 'roles', 'dept']