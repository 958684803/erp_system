from django.db import models

from erp_system.utils.basemodel import BaseModel


# Create your models here.

# 创建菜单模型类
class MenuModel(BaseModel):
    number = models.IntegerField(verbose_name='排序数字', blank=True, null=True)
    url = models.CharField(verbose_name='菜单访问的url', max_length=256, blank=True, null=True)
    delete_flag = models.CharField(verbose_name='标记删除', max_length=1, default="o")
    name = models.CharField(verbose_name='菜单名字', max_length=50)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 't_menu'
        verbose_name = '菜单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
