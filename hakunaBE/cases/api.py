import requests
import json
from typing import List
from wsgiref import headers
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from hakunaBE.customPagination import CustomPagination
from module.models import Module
from cases.models import Cases
from cases.api_schema import CaseIn, CaseDebugIn, CaseAssertIn, CaseOut
from ninja import Router
from ninja.pagination import paginate
from hakunaBE.common import Error, response


router = Router(tags=['cases'])

@router.post("/", auth=None)
def case_create(request, data:CaseIn):
    """创建用例"""
    module = Module.objects.filter(id=data.module_id, is_delete=False)
    if len(module) == 0:
        return response(error = Error.MODULE_NOT_EXIST)

    newCase = Cases.objects.create(**data.dict())
    return response(item=model_to_dict(newCase))


@router.post("/debug/")
def case_debug(request, data:CaseDebugIn):
    """调试用例"""
    url = data.url
    method =data.method.lower()
    header = data.header
    params_type = data.params_type
    params_body = data.params_body

    if method == "get":
        resp = requests.get(url, headers=header, params=params_body).text
    if method == "post":
        if params_type == 'form':
            resp = requests.post(url, headers=header, data=params_body).text
        elif params_type == 'json':
            resp = requests.post(url, headers=header, json=params_body).text
        else:
            return response(error=Error.CASES_PARAMS_ERROR)

    if method == "put":
        if params_type == 'form':
            resp = requests.put(url, headers=header, data=params_body).text
        elif params_type == 'json':
            resp = requests.put(url, headers=header, json=params_body).text
        else:
            return response(error=Error.CASES_PARAMS_ERROR)

    if method == "delete":
        if params_type == 'form':
            resp = requests.delete(url, headers=header, data=params_body).text
        elif params_type == 'json':
            resp = requests.delete(url, headers=header, json=params_body).text
        else:
            return response(error=Error.CASES_PARAMS_ERROR)

    return response(item={'response':resp})


@router.post("/assert/")
def case_assert(request, data:CaseAssertIn):
    """用例断言"""
    print('data', data)
    resp = data.response
    assert_type = data.assert_type
    assert_text = data.assert_text

    if assert_type == 'include':
        if assert_text in resp:
            return response()
        else:
            return response(success=False)
    elif assert_type == 'equal':
        if assert_text == resp:
            return response()
        else:
            return response(success=False)
    return response()


@router.delete("/{case_id}/")
def case_delete(request, case_id: int):
    """用例删除"""
    case = get_object_or_404(Cases, id=case_id)
    case.is_delete = True
    case.save()
    return response()

@router.put("/{case_id}/")
def case_update(request, case_id: int, data: CaseIn):
    """修改用例信息"""
    case = get_object_or_404(Cases, id = case_id)
    for attr, value in data.dict().items():
        setattr(case, attr, value)
    case.save()
    return response()

@router.get('/{case_id}/')
def get_case(request, case_id: int):
    """获取用例"""
    case = get_object_or_404(Cases, id = case_id)
    return response(item=model_to_dict(case))


@router.get('/{module_id}/cases', response=List[CaseOut])
@paginate(CustomPagination)
def get_case_list(request, module_id: int, **kwargs):
    """获取模块下的用例列表"""
    return Cases.objects.filter(module_id=module_id, is_delete=False)
