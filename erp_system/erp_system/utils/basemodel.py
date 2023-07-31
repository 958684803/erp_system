from django.db import models


# 创建父类
class BaseModel(models.Model):
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    class Meta:
        abstract = True  # 不会映射到数据库
