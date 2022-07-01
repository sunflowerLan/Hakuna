
from django.db import IntegrityError
from typing import List
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from ninja import Query, Router
from ninja.pagination import paginate
from cases.models import TestCase
from hakunaBE.common import Error, response
from hakunaBE.customPagination import CustomPagination
from tasks.models import TaskCaseRelevance, TestResult, TestTask
from .api_shema import ResultOut, TestTaskIn, TaskOut
from projects.models import Project
from tasks.task_running.test_running import async_run_task
import json


router = Router(tags=['tasks'])

@router.get('/{project_id}/list/', response=List[TaskOut])
@paginate(CustomPagination)
def get_task_list(request,  project_id: int, **kwargs):
    """
    获取项目列表
    auth=None 该接口不需要认证
    """
    task_list = TestTask.objects.filter(project_id=project_id, is_delete=False).all()
    for task in task_list:
        relevance = TaskCaseRelevance.objects.get(task_id=task.id)
        task.cases = json.loads(relevance.case)
    return task_list

@router.post('/')
def task_create(request, data: TestTaskIn):
    """创建测试任务"""
    project = get_object_or_404(Project, pk=data.project)
    newTask = TestTask.objects.create(project=project, name = data.name, describe = data.describe)
    cases = []
    cases_json = json.dumps(data.cases)
    TaskCaseRelevance.objects.create(task_id=newTask.id, case=cases_json)
    task_dict = model_to_dict(newTask)
    task_dict["cases"] = cases
    return response(item=task_dict)


@router.post('/{task_id}/running')
def task_running(request, task_id: int):
    """执行测试任务"""
    # 获取测试任务
    task = get_object_or_404(TestTask, pk = task_id)
    # 改写任务状态：执行中
    task.status = 1
    task.save()

    # 异步执行测试任务
    async_run_task(task.id)
    return response()


@router.get('/{task_id}/')
def get_task_detail(request, task_id: int):
    """获取任务详情"""
    task = get_object_or_404(TestTask, pk=task_id)
    if task.is_delete is True:
        return response(error=Error.TASK_IS_DELETE)
    
    relevance = TaskCaseRelevance.objects.filter(task_id=task.id)[0]
    task_dict = model_to_dict(task)
    task_dict["cases"] = json.loads(relevance.case)
    return response(item=task_dict)


@router.put('/{task_id}/')
def task_update(request, task_id: int , data: TestTaskIn):
    """更新测试任务"""
    project = get_object_or_404(Project, pk = data.project, is_delete=False)

    task = get_object_or_404(TestTask, pk = task_id)
    task.name = data.name
    task.describe = data.describe
    task.project = project
    task.save()

    # 更新关系
    relevance = TaskCaseRelevance.objects.filter(task_id = task_id)[0]
    relevance.case = json.dumps(data.cases)
    relevance.save()

    task_dict = model_to_dict(task)
    task_dict["cases"] = data.cases

    # 建立新的关系
    # for case_id in data.case_id_list:
    #     try:
    #         TaskCaseRelevance.objects.create(task_id=task.id, case_id=case_id)
    #     except IntegrityError:
    #         return response(error=Error.CASE_NOT_EXIST)
    return response(item=task_dict)


@router.delete('/{task_id}/')
def task_delete(request, task_id: int):
    """删除测试任务"""
    task = get_object_or_404(TestTask, pk = task_id)
    task.is_delete = True
    task.save()
    return response()


@router.get('/{task_id}/results/', response=List[ResultOut])
@paginate(CustomPagination)
def get_task_result(request, task_id: int, **kwargs):
    """获取任务的所有运行结果"""
    task = get_object_or_404(TestTask, pk=task_id)
    return TestResult.objects.filter(task=task).all()