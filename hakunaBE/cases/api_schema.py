from datetime import datetime
from typing_extensions import assert_type
from ninja import Schema

from hakunaBE.common import response


class CaseIn(Schema):
    """用例入参"""
    name: str
    module_id: int
    url: str
    method: str
    header: str
    params_type: str
    params_body: str
    response: str
    assert_type: str
    assert_text: str


class CaseDebugIn(Schema):
    """用例调试入参"""
    url: str
    method: str
    header: dict
    params_type: str
    params_body: dict


class CaseAssertIn(Schema):
    """用例调试入参"""
    response: str
    assert_type: str
    assert_text: str


class CaseOut(Schema):
    """用例出参"""
    id: int
    name: str
    create_time: datetime