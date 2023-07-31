from rest_framework.pagination import PageNumberPagination


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,  # 返回jwt签发的token
        'id': user.id, # 返回用户ID
        'username': user.username  # 返回用户的用户名
    }