from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


# 批量删除
class BatchDestroy:
    """
    批量删除的类
    """

    del_ids = openapi.Schema(type=openapi.TYPE_OBJECT, required=['ids'], properties={
        'ids': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_INTEGER),
                              description='需要删除的菜单id列表')
    })

    @swagger_auto_schema(methods=['delete'], request_body=del_ids)
    @action(methods=['delete'], detail=False)
    def batchdestroy(self, request, *args, **kwargs):
        ids = request.data.get('ids', None)
        if not ids:
            return Response(data={"detail": "参数错误，ids为必传参数"}, status=status.HTTP_400_BAD_REQUEST)
        elif not isinstance(ids, list):
            return Response(data={"detail": "参数错误，ids必须为列表"}, status=status.HTTP_400_BAD_REQUEST)
        # 先获得查询集queryset
        queryset = self.get_queryset()  # 这个queryset是在视图中子类会传过来
        # 再删除传递过来的功能菜单
        del_queryset = queryset.filter(id__in=ids)
        # 判断del_queryset的数量是否等于ids的长度
        if del_queryset.count() != len(ids):
            return Response(data={"detail": "参数错误，ids中有不存在的id"}, status=status.HTTP_400_BAD_REQUEST)
        del_queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
