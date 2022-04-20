
from ninja import Schema


class TestTaskIn(Schema):
    """测试任务入参"""
    project: int
    name: str
    describe: str = None
    case_id_list: list # 用例id [1,3,5]