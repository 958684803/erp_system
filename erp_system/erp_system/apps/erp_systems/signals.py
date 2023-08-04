import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from erp_systems.models import MenuModel, PermissionModel

logger = logging.getLogger('erp')

methods = {
    "GET": "查询",
    "POST": "新增",
    "PUT": "修改",
    "DELETE": "删除",
    "PATCH": "局部修改"
}


@receiver(post_save, sender=MenuModel)
def create_menu_permission(sender, instance, created, **kwargs):
    """
    创建菜单时为菜单添加权限
    """
    if created:
        logger.info("创建菜单时为菜单添加权限")
        if isinstance(instance, MenuModel):
            if not instance.parent:  # 没有父id，说明是顶级菜单
                # 顶级菜单的权限
                permission = PermissionModel.objects.create(name=instance.name + '的权限', is_menu=True)
                permission.menu = instance
                permission.save()
            else:  # 有父id，说明是子菜单
                # 给所有的子菜单添加所有的methd方法的权限
                for method in methods.keys():
                    permission = PermissionModel.objects.create(name=f"{instance.name}的{methods[method]}的权限",
                                                                is_menu=False,
                                                                method=method,
                                                                path=instance.url)
                    permission.menu = instance
                    permission.save()
        else:
            logger.warning("创建菜单时为菜单添加权限时，传入的参数不是MenuModel的实例")
