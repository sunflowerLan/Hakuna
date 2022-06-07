
from distutils.log import error
from typing import Any
from ninja import Schema


class TestTaskIn(Schema):
    """测试任务入参"""
    project: int
    name: str
    describe: str = None
    case_id_list: list # 用例id [1,3,5]


class ResultOut(Schema):
    """测试报告返回"""
    name: str
    passed: int
    error: int
    failure: int
    skipped: int
    tests: int
    run_time: float
    result: str
    create_time: Any