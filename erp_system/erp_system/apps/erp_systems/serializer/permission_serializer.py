from rest_framework import serializers, status
from rest_framework.response import Response

from erp_system.utils.batch_destroy import BatchDestroy
from erp_systems.models import PermissionModel


class PermissionSerializer(serializers.ModelSerializer, BatchDestroy):
    """
    权限模型的序列化器
    """
    class Meta:
        model = PermissionModel
        fields = '__all__'
