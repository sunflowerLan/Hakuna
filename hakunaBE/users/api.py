
from ninja import Router
from users.api_schema import RegisterIn, LoginIn
from hakunaBE.common import response, Error
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.sessions.models import Session


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
    return response(item=user_info)

@router.post('/login', auth=None)
def user_login(request, payload: LoginIn):
    """
    用户登陆
    auth=None 该接口不需要认证
    """
    username = payload.username
    password = payload.password
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user) # 会向session表创建一条数据
        token = Session.objects.last() # last 最近的一条数据
        user_info = {
            "id": user.id,
            "username": user.username,
            "token": token.session_key
        }
        return response(item=user_info)
    else:
        return response(error=Error.USER_OR_PWD_ERROR)


@router.get('/logout')
def user_logout(request):
    """用户退出"""
    auth.logout(request)
    pass


@router.get("/bearer")
def bearer(request):
    """
    假设，必须要登录之后才能访问
    测试：获取token
    """
    return {"token": request.auth}