from datetime import datetime
from ninja import NinjaAPI
from ninja.security import HttpBearer
from django.contrib.sessions.models import Session
from users.api import router as users_router
from projects.api import router as projects_router
from module.api import router as module_router
from cases.api import router as cases_router

class InvalidToken(Exception):
    """无效的token"""
    pass

class ExpiredToken(Exception):
    """过期的token"""
    pass


class GlobalAuth(HttpBearer):

    def authenticate(self, request, token):
        """
        自定义认证token处理
        """
        session = Session.objects.filter(pk=token).first()
        if session is None:
            raise InvalidToken
        expire_date = session.expire_date
        now = datetime.now()
        # datetime.now().timestamp() > parse(expire_date).timestamp()
        if not now < expire_date.replace(tzinfo=None): # 转换为无时区时间进行比对
            raise ExpiredToken

        return token


api = NinjaAPI(auth=GlobalAuth())

@api.exception_handler(InvalidToken)
def on_invalid_token(request, exc):
    """无效token返回类型"""
    return api.create_response(request, {"detail": "Invalid token supplied"}, status=401)

@api.exception_handler(ExpiredToken)
def on_expired_token(request, exc):
    """过期token返回类型"""
    return api.create_response(request, {"detail": "Expired token supplied"}, status=401)


# tags users  URI: api/vi/users/xxx
api.add_router('/users/', users_router)
# tags projects  URI: api/vi/projects/xxx
api.add_router('/projects/', projects_router)
# tags module  URI: api/vi/module/xxx
api.add_router('/module/', module_router)
# tags cases  URI: api/vi/cases/xxx
api.add_router('/cases/', cases_router)