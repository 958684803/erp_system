"""
URL configuration for erp_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.documentation import include_docs_urls

# schema_view = get_schema_view(
#     # 具体定义详见 [Swagger/OpenAPI 规范](https://swagger.io/specification/#infoObject)
#     openapi.Info(
#         title="Snippets API",
#         default_version='v1',
#         description="Test description",
#         terms_of_service="https://www.google.com/policies/terms/",
#         contact=openapi.Contact(email="contact@snippets.local"),
#         license=openapi.License(name="BSD License"),
#     ),
#     # public 表示文档完全公开, 无需针对用户鉴权
#     public=True,
#     # 可以传递 drf 的 BasePermission
#     permission_classes=(permissions.AllowAny,),
# )
#
urlpatterns = [
    re_path(r'^user/login/$', obtain_jwt_token),  # JWT签发和认证视图
    re_path(r'^', include('erp_systems.urls')),
	path('docs/', include_docs_urls(title='站点页面标题')),
# drf_yasg
#     re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-spec'),
#     re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#     re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
