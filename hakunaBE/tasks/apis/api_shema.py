
from typing import Any, List
from ninja import Schema


class TestTaskIn(Schema):
    """测试任务入参"""
    project: int
    name: str
    describe: str = None
    cases: list # 用例id [1,3,5]


class TaskOut(Schema):
    """测试任务出参"""
    id: int
    name: str
    status: int
    describe: str = None
    create_time: Any
    update_time: Any
    cases: List

class ResultOut(Schema):
    """测试报告返回"""
    id: int
    name: str
    passed: int
    error: int
    failure: int
    skipped: int
    tests: int
    run_time: float
    result: str
    create_time: Any