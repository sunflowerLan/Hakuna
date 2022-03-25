import os
import hashlib
from django.shortcuts import get_object_or_404
from ninja import File, Router
from ninja.files import UploadedFile
from ninja.pagination import paginate
from hakunaBE.customPagination import CustomPagination
from hakunaBE.common import response, Error
from projects.api_schema import ProjectIn, ProjectOut
from projects.models import Project
from hakunaBE.settings import IMAGE_DIR
from typing import List

router = Router(tags=["projects"])
FILE_TYPE = ['img', 'png', 'jpg', 'jpeg']

@router.post('/')
def create_project(request, payload: ProjectIn):
    """
    创建项目
    """
    project = Project.objects.filter(name=payload.name)
    if len(project) > 0:
        return response(error=Error.PROJECT_NAME_EXIST)

    project = Project.objects.create(**payload.dict())
    return response(result={"id": project.id})

@router.get('/list', response=List[ProjectOut])
@paginate(CustomPagination, page_size=6)
def project_lists(request, **kwargs):
    """
    获取项目列表
    """
    data = [
        {
            "id": p.id,
            "name": p.name,
            "describe": p.describe,
            "image": p.image,
            "create_time": p.create_time
        
        }
        for p in Project.objects.filter(is_delete=False).order_by('-update_time')
    ]
    return data

@router.get('/{project_id}')
def project_details(request, project_id: int):
    """
    获取项目详情
    """
    project = get_object_or_404(Project, id=project_id)
    if project.is_delete:
        return response(error = Error.PROJECT_IS_DELETE)
    
    data = {
            "id": project.id,
            "name": project.name,
            "describe": project.describe,
            "image": project.image,
            "create_time": project.create_time
    }
    return response(result=data)

@router.put('/{project_id}')
def project_update(request, project_id: int, payload: ProjectIn):
    """
    更新项目
    """
    project = get_object_or_404(Project, id=project_id)
    for attr, value in payload.dict().items():
        setattr(project, attr, value)
    project.save()
    return response()

@router.delete('/{project_id}')
def project_delete(request, project_id: int):
    """
    删除项目
    """
    project = get_object_or_404(Project, id=project_id)
    project.is_delete = True
    project.save()
    return response()

@router.post("/upload/")
def project_image_upload(request, file: UploadedFile= File(...)):
    """
    项目图片上传
    """
    # 判断文件后缀
    suffix = file.name.split('.')[-1]
    if suffix not in FILE_TYPE:
        return response(error=Error.FILE_TYPE_ERROR)
    
    # 判断文件大小 1024 * 1024 * 2 = 2MB
    if file.size > 2097152:
        return response(error=Error.FILE_SIZE_ERROR)
    
    # 文件名生成md5
    file_md5 = hashlib.md5(bytes(file.name, encoding='utf-8')).hexdigest()
    file_name = file_md5 + "." + suffix

    # 保存到本地
    upload_file = os.path.join(IMAGE_DIR, file_name)
    with open(upload_file, 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)

    return response(result={"name": file_name})