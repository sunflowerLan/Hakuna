from ninja import Schema


class RegisterIn(Schema):
    '''用户注册入参'''
    username: str
    password: str
    confirm_password: str

class LoginIn(Schema):
    username: str
    password: str