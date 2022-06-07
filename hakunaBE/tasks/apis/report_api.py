
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from ninja import Router
from hakunaBE.common import response
from tasks.models import TestResult


router = Router(tags=['reports'])


@router.get('/{report_id}/')
def report_detail(request, report_id: int):
    """获取测试结果详情"""
    result = get_object_or_404(TestResult, pk = report_id)
    return response(item=model_to_dict(result))


@router.delete('/{report_id}/')
def report_delete(request, report_id: int):
    """删除测试报告"""
    result = get_object_or_404(TestResult, pk = report_id)
    result.delete()
    return response()