import os
import json
from cases.models import TestCase
from tasks.models import TaskCaseRelevance, TestTask
import threading
from tasks.task_running.test_result import save_test_result
from hakunaBE.settings import BASE_DIR

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA = os.path.join(BASE_DIR, "tasks", "task_running", "test_data.json")
TEST_CASE = os.path.join(BASE_DIR, "tasks", "task_running", "test_case.py")


def running(task_id: int):
    """执行任务"""
    # 1. 读取测试用例
    print("1. 读取测试用例")
    relevance = TaskCaseRelevance.objects.get(task_id=task_id)
    relevance_list = json.loads(relevance.case)
    # [{"moduleId": 1, "casesId": [1, 2, 3]}, {"moduleId": 6, "casesId": [5, 6]}]
    case_ids = []
    for rel in relevance_list:
      case_ids = case_ids + rel["casesId"]

    test_cases = {}
    for cid in case_ids:
        try:
            case = TestCase.objects.get(pk=cid, is_delete=False)
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

    # 2. 用例数据写入json文件
    print("2. 用例数据写入json文件")
    with open(TEST_DATA, 'w', encoding='utf-8') as f:
        # f.write(json.dumps(test_cases, ensure_ascii=False))
        json.dump(test_cases, f, ensure_ascii=False)

    # 3. 执行用例
    print("3. 执行用例")
    os.system(f"python3 {TEST_CASE}")

    # 4. 保存测试结果
    print("4. 保存测试结果")
    save_test_result(task_id)

    # 5. 执行完用例，改写任务状态
    print("5. 改写任务状态: 已完成")
    task = TestTask.objects.get(id=task_id)
    task.status = 2
    task.save()


def async_run(task_id: int):
    """
    异步执行任务
    守护进程，等待用例执行完
    """
    threads = []
    t = threading.Thread(target=running, args=(task_id, ))
    threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join() #守护进程, 等待用例执行完


def async_run_task(task_id: int):
    """
    异步执行
    """
    threads = []
    t = threading.Thread(target=async_run, args=(task_id, ))
    threads.append(t)
    for t in threads:
        t.start()