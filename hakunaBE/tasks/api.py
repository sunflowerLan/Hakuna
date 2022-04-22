import json
import os
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from ninja import Router
from cases.models import TestCase
from hakunaBE.common import response
from hakunaBE.settings import BASE_DIR

from tasks.models import TaskCaseRelevance, TestTask
from .api_shema import TestTaskIn
from projects.models import Project
from tasks.task_running.test_result import save_test_result


TEST_DATA = os.path.join(BASE_DIR, "tasks", "task_running", "test_data.json")
TEST_RUNNING = os.path.join(BASE_DIR, "tasks", "task_running", "test_running.py")
router = Router(tags=['tasks'])

@router.post('/')
def task_create(request, data: TestTaskIn):
    """创建测试任务"""
    project = get_object_or_404(Project, pk=data.project)
    newTask = TestTask.objects.create(project=project, name = data.name, describe = data.describe)
    cases = []
    for case_id in data.case_id_list:
        TaskCaseRelevance.objects.create(task_id = newTask.id, case_id = case_id)
        case = TestCase.objects.get(pk=case_id)
        cases.append({
            "case": case.id,
            "module": case.module_id
        })
    task_dict = model_to_dict(newTask)
    task_dict["cases"] = cases
    return response(item=task_dict)


@router.post('/{task_id}/running')
def task_running(request, task_id: int):
    """执行测试任务"""
    # 1. 获取测试任务
    task = get_object_or_404(TestTask, pk = task_id)

    # 2. 读取测试用例
    rel_list = TaskCaseRelevance.objects.filter(task_id = task.id)
    test_cases = {}
    for rel in rel_list:
        try:
            case = TestCase.objects.get(pk=rel.case_id)
            header_str = json.loads(case.header.replace("\'", "\""))
            params_body_str = json.loads(case.params_body.replace("\'", "\""))
            test_cases[case.name] = {
                "url": case.url,
                "method": case.method,
                "header": header_str,
                "params_type": case.params_type,
                "params_body": params_body_str,
                "assert_type": case.assert_type,
                "assert_text": case.assert_text
            }
        except TestCase.DoesNotExist:
            pass
    # print("test_cases: ", test_cases)

    # 3. 用例数据写入json文件
    with open(TEST_DATA, 'w', encoding='utf-8') as f:
        # f.write(json.dumps(test_cases, ensure_ascii=False))
        json.dump(test_cases, f, ensure_ascii=False)

    # 4. 执行用例
    os.system(f"python {TEST_RUNNING}")

    # 5. 保存测试结果
    save_test_result(task_id)

    return response()