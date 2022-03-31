from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from cases.models import Module
from projects.models import Project
from cases.api_schema import ModuleIn
from ninja import Router
from hakunaBE.common import Error, response

router = Router(tags=['cases'])

@router.post("/module/", auth=None)
def module_create(request, data:ModuleIn):
    """创建模块"""
    project = Project.objects.filter(id=data.project_id, is_delete=False)
    if len(project) == 0:
        return response(error = Error.PROJECT_NOT_EXIST)
    
    module = Module.objects.filter(name=data.name, project_id=data.project_id)
    if len(module) > 0 :
        return response(error= Error.MODULE_NAME_EXIST)
    
    newModule = Module.objects.create(**data.dict())
    return response(item=model_to_dict(newModule))


@router.delete("/module/{module_id}/")
def module_delete(request, module_id: int):
    """模块删除"""
    module = get_object_or_404(Module, id=module_id)
    module.is_delete = True
    module.save()
    return response()

@router.put("/module/{module_id}/")
def module_update(request, module_id: int, data: ModuleIn):
    """修改模块信息"""
    module = get_object_or_404(Module, id = module_id)
    for attr, value in data.dict().items():
        setattr(module, attr, value)
    module.save()
    return response()


def node_tree(nodes, current_node):
    """递归：获取某个节点下的所有子节点"""
    for node in nodes:
        if node['parent_id'] == current_node['id']:
            current_node["children"].append(node)
            node_tree(nodes, node)
    return current_node


@router.get('/{project_id}/module/tree')
def get_module_tree(request, project_id: int):
    """获取模块树"""
    modules = Module.objects.filter(project_id=project_id, is_delete=False)

    if len(modules) == 0:
        return response(error = Error.MODULE_NOT_EXIST)
    roots = [] # 根节点
    nodes = [] # 子节点
    for module in modules: # 分别查找出所有的根节点和子节点
        data = {
            "id": module.id,
            "label": module.name,
            "parent_id": module.parent_id,
            "children": []
        }
        if module.parent_id == 0:
            roots.append(data)
        else:
            nodes.append(data)
    # print("--------> roots:", roots)
    # print("--------> nodes:", nodes)

    data_tree = []
    for root in roots: # 循环根节点
        data_children = node_tree(nodes, root) # 循环遍历子节点，为每个根节点查找子节点
        data_tree.append(data_children) #根节点添加到结构数队列中

    return response(item=data_tree)

