from datetime import datetime
from ninja import Schema


class ModuleIn(Schema):
    """模块入参"""
    name: str
    project_id: int
    parent_id: int = 0


class ModuleOut(Schema):
    """模块出参"""
    id: int
    name: str
    create_time: datetime