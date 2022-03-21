
from ninja import Router
from users.api_schema import RegisterIn, LoginIn
from hakunaBE.common import response, Error
from django.contrib.auth.models import User


router = Router(tags=["users"])

@router.post('/register', auth=None)
def user_register(request, data: RegisterIn):
    """
    用户注册
    auth=None 该接口不需要认证
    """
    username = data.username
    password = data.password
    confirm_password = data.confirm_password

    if password != confirm_password:
        return response(error=Error.PWD_ERROR)
    
    try:
        User.objects.get_by_natural_key(username)
    except User.DoesNotExist:
        pass
    else:
        return response(error=Error.USER_EXIST)
    
    user = User.objects.create_user(username=username, password=password)
    user_info = {
        "id": user.id,
        "username": username
    }
    return response(result=user_info)