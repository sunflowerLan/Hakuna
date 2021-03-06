from itertools import chain


class Error:
    """
    自定义错误与错误信息
    """
    TOKEN_ERROR = {"10300": "认证失败"}

    USER_OR_PWD_NULL = {"10010": "用户名密码为空"}
    USER_OR_PWD_ERROR = {"10011": "用户名密码错误"}
    PWD_ERROR = {"10012": "两次密码不一致"}
    USER_EXIST = {"10013": "用户名已经被注册"}

    PROJECT_NAME_EXIST = {"10021": "项目名称已存在"}
    PROJECT_NOT_EXIST = {"10022": "项目不存在"}
    PROJECT_IS_DELETE = {"10023": "项目已经被删除"}

    FILE_TYPE_ERROR = {"10031": "文件类型错误"}
    FILE_SIZE_ERROR = {"10032": "超出文件大小"}
    FILE_NOT_EXIST = {"10033": "文件不存在"}

    MODULE_NAME_EXIST = {"10041": "模块名称已存在"}
    MODULE_NOT_EXIST = {"10042": "当前项目下没有模块"}
    MODULE_IS_DELETE = {"10043": "模块已经被删除"}

    CASES_METHOD_ERROR = {"10051": "请求方法错误"}
    CASES_HEADER_ERROR = {"10052": "请求header错误"}
    CASES_PARAMS_ERROR = {"10053": "请求参数类型错误"}

    TASK_IS_DELETE = {"10061": "测试任务已删除"}

def model_to_dict(instance: object) -> dict:
    """
    对象转字典
    """
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        data[f.name] = f.value_from_object(instance)
    return data

def response(success: bool = True, error = None, item=None) -> dict:
    """
    定义统一返回格式
    """
    if error is None:
        error_code = ""
        error_msg = ""
    else:
        success = False
        error_code = list(error.keys())[0]
        error_msg = list(error.values())[0]
    
    if item is None:
        item = {}

    resp_data = {
        "success": success,
        "error": {
            "code": error_code,
            "msg": error_msg
        },
    }

    if isinstance(item, dict):
        resp_data["item"] = item
    elif isinstance(item, list):
        resp_data["items"] = item
    elif isinstance(item, object):
        item = model_to_dict(item)
        resp_data["item"] = item
    else:
        resp_data["item"] = {}
    return resp_data