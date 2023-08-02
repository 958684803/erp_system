from django.contrib.auth.backends import ModelBackend

from erp_systems.models import UserModel


class UserLoginAuth(ModelBackend):
    """
    自定义用户登录验证，重写ModelBackend
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(username=username)
        except:
            return None

        if user.check_password(password):
            return user
        else:
            return None
