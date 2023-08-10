from rest_framework import serializers

from erp_system.utils.batch_destroy import BatchDestroy
from erp_systems.models import DeptModel


class DeptSerializer(serializers.ModelSerializer, BatchDestroy):
    """
    部门的序列化器
    """
    # 重新定义一下时间格式
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = DeptModel
        fields = '__all__'
