from cases.models import Module
from projects.models import Project
from cases.api_schema import ModuleIn
from ninja import Router
from hakunaBE.common import Error, response

router = Router(tags=['cases'])

@router.post("/", auth=None)
def create_module(request, data:ModuleIn):
    """创建模块"""
    project = Project.objects.filter(id=data.project_id)
    if len(project) == 0:
        return response(error = Error.PROJECT_NOT_EXIST)
    module = Module.objects.filter(name=data.name, project_id=data.project_id)
    if len(module) > 0 :
        return response(error= Error.MODULE_NAME_EXIST)
    Module.objects.create(**data.dict())
    return response(result={"id": module.id})


@router.get('/cases')
def get_module_tree(request, data:ModuleIn):
    """获取模块树"""
    pass
