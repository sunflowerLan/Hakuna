
from django.forms import model_to_dict
from typing import List
from django.shortcuts import get_object_or_404
from hakunaBE.customPagination import CustomPagination
from ninja.pagination import paginate
from ninja import Router
from hakunaBE.common import response
from tasks.apis.api_shema import ResultOut
from tasks.models import TestResult, TestTask


router = Router(tags=['reports'])


@router.get('/{project_id}/list/', response=List[ResultOut])
@paginate(CustomPagination)
def get_report_list(request,  project_id: int, **kwargs):
    """
    获取项目列表
    auth=None 该接口不需要认证
    """
    tasks = TestTask.objects.filter(project_id=project_id, is_delete=False).all()
    report_list = []
    for task in tasks:
        # print("task id=>", task.id)
        reports = TestResult.objects.filter(task_id=task.id).all()
        for report in reports:
            # print("report id", report.id)
            report_list.append(report)
    return report_list


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