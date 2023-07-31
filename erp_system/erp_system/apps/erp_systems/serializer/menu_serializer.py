from rest_framework import serializers

from erp_systems.models import MenuModel


class MenuSerializer(serializers.ModelSerializer):
    """
    功能菜单的序列化器
    """

    class Meta:
        model = MenuModel
        fields = '__all__'
