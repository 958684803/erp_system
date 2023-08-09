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

from django.urls import path, re_path
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from erp_systems.views.menu_view import MenuView
from erp_systems.views.permission_view import PermissionViewSet
from erp_systems.views.role_view import RoleViewSet
from erp_systems.views.user_view import RegisterUserView

urlpatterns = [
    re_path(r'^user/login/$', obtain_jwt_token),  # JWT签发和认证视图
    re_path(r'^user/register/$', RegisterUserView.as_view()),  # 用户注册视图

]

router = routers.DefaultRouter()
router.register(r'menu', MenuView)  # 菜单路由
router.register(r'permission', PermissionViewSet)  # 权限路由
router.register(r'role', RoleViewSet)  # 角色路由
print(router.urls)
urlpatterns += router.urls
