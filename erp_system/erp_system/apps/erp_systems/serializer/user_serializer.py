import re

from rest_framework import serializers, mixins
from rest_framework.exceptions import ValidationError

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


class UpdatePassWordSerializer(serializers.ModelSerializer):
    """
    用户修改密码的序列化器
    """
    new_password = serializers.CharField(label='新密码', min_length=6, max_length=20, write_only=True)
    confirm_password = serializers.CharField(label='确认密码', min_length=6, max_length=20, write_only=True)

    class Meta:
        model = UserModel
        fields = ['id', 'password', 'new_password', 'confirm_password']

        extra_kwargs = {
            'password': {'write_only': True},
            'new_password': {'write_only': True},
            'confirm_password': {'write_only': True},
        }

    def validate(self, attrs):
        # 先验证传过来的密码是否正确
        if not attrs.get('password'):
            raise ValidationError('密码不能为空')
        elif not attrs.get('new_password'):
            raise ValidationError('新密码不能为空')
        elif not attrs.get('confirm_password'):
            raise ValidationError('确认密码不能为空')
        elif attrs.get('new_password') != attrs.get('confirm_password'):
            raise ValidationError('两次密码不一致')
        return attrs

    def save(self, **kwargs):
        if not self.instance.check_password(self.validated_data.get('password')):
            raise ValidationError('原密码错误')
        self.instance.set_password(self.validated_data.get('new_password'))
        self.instance.save()
        return self.instance