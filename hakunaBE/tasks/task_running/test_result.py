
import os
import xml.etree.ElementTree as ET
from tasks.models import TestResult

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_REPORT = os.path.join(BASE_DIR, "xml_result.xml")


def save_test_result(task_id):
    """保存测试结果"""
    # 解析xml文件
    tree = ET.parse(TEST_REPORT)

    # 根节点
    root = tree.getroot()

    # testsuite 节点
    testsuite = root[0]
    # 获取属性
    name = testsuite.get('name')
    time = testsuite.get('time')
    tests = testsuite.get('tests')
    errors = testsuite.get('errors')
    failures = testsuite.get('failures')
    skipped = testsuite.get('skipped')
    passed = int(tests) - int(errors) - int(failures) - int(skipped)

    with open(TEST_REPORT, "r") as f:
        result = f.read()

        TestResult.objects.create(
            task_id=task_id,
            name=name,
            passed=passed,
            error=errors,
            failure=failures,
            skipped=skipped,
            tests=tests,
            run_time=time,
            result=result,
        )
