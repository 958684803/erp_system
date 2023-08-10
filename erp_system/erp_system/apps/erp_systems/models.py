from django.contrib.auth.models import AbstractUser
from django.db import models

from erp_system.utils.basemodel import BaseModel


# Create your models here.

# 创建菜单模型类
class MenuModel(BaseModel):
    number = models.IntegerField(verbose_name='排序数字', blank=True, null=True)
    url = models.CharField(verbose_name='菜单访问的url', max_length=256, blank=True, null=True)
    delete_flag = models.CharField(verbose_name='标记删除', max_length=1, default="0")
    name = models.CharField(verbose_name='菜单名字', max_length=50)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 't_menu'
        verbose_name = '菜单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class UserModel(AbstractUser):
    """
    用户模型类
    """
    phone = models.CharField(verbose_name='手机号', max_length=11, blank=True, null=True)
    real_name = models.CharField(verbose_name='真实姓名', max_length=50, blank=True, null=True)
    roles = models.ManyToManyField('RoleModel', verbose_name='用户拥有的角色', blank=True)
    dept = models.ForeignKey('DeptModel', verbose_name='用户所属部门', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 't_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class PermissionModel(BaseModel):
    """
    权限模型类
    """

    choice_methods = (
        ('GET', '查'),
        ('POST', '增'),
        ('PUT', '改'),
        ('DELETE', '删'),
        ('PATCH', '局部修改')
    )
    is_menu = models.BooleanField(verbose_name='是否是菜单', default=False)
    name = models.CharField(verbose_name='权限名字', max_length=50)
    method = models.CharField(verbose_name='请求方法', max_length=10, choices=choice_methods, blank=True, null=True)
    path = models.CharField(verbose_name='权限访问的url', max_length=256, blank=True, null=True)
    menu = models.ForeignKey('MenuModel', on_delete=models.CASCADE, blank=True, null=True)
    desc = models.CharField(verbose_name='权限描述', max_length=256, blank=True, null=True)

    class Meta:
        db_table = 't_permission'
        verbose_name = '权限'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name


class RoleModel(BaseModel):
    """
    角色模型类
    """
    name = models.CharField(verbose_name='角色名字', max_length=50)
    permissions = models.ManyToManyField('PermissionModel', verbose_name='角色拥有的权限', blank=True)

    class Meta:
        db_table = 't_role'
        verbose_name = '角色'
        verbose_name_plural = verbose_name
        ordering = ['id']


def __str__(self):
    return self.name


class DeptModel(BaseModel):
    """
    部门模型类
    """
    name = models.CharField(verbose_name='部门名字', unique=True, max_length=50)
    address = models.CharField(verbose_name='部门地址', max_length=50, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 't_dept'
        verbose_name = '部门'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name