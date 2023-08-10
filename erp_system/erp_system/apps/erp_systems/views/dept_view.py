from rest_framework import viewsets

from erp_system.utils.batch_destroy import BatchDestroy
from erp_system.utils.global_page import GlobalPagination
from erp_systems.models import DeptModel
from erp_systems.serializer.dept_serializer import DeptSerializer


class DeptViewSet(viewsets.ModelViewSet, BatchDestroy):
    """
    list:
    部门--获取列表

    获取部门列表，status：200（成功），return：部门列表

    create:
    部门--新增

    部门新增，status：201（成功），return：新增部门信息

    read:
    部门--获取某个部门的详情

    获取某个部门的详情，status：200（成功），return：某个部门的详情
    update:
    部门--修改

    部门修改，status：200（成功），return：修改后的部门信息

    partial_update:
    部门--部分修改

    部分部门修改，status：200（成功），return：修改后的部门信息

    delete:
    部门--删除

    部门删除，status：204（成功），return：空

    batchdestroy:
    部门--批量删除

    部门批量删除，status：204（成功），return：空

    get_menu_id_permission:
    部门--根据菜单的id查询当前菜单或者接口的所部门有

    根据菜单的id查询当前菜单或者接口的所有部门，status：200（成功），return：当前菜单或者接口的所部门有
    """

    queryset = DeptModel.objects.all()
    serializer_class = DeptSerializer
    # 分页器
    pagination_class = GlobalPagination

    # pid=0查询所有的父部门
    # pid!=0查询某个父部门下面的所有子部门
    # pid=None查询所有的部门
    def get_queryset(self):
        query_param = self.request.query_params.get('pid', None)
        if query_param:
            pid = int(query_param)
            if pid == 0:
                return DeptModel.objects.filter(parent__isnull=True).all()
            else:
                return DeptModel.objects.filter(parent_id=pid).all()
        else:
            return DeptModel.objects.all()
