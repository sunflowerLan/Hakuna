
from django.db import models
from projects.models import Project

# Create your models here.
class Module(models.Model):
    """
    模块表
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField("名称", max_length=100, null=False, default="")
    parent_id = models.IntegerField("父级ID", default=0)
    is_delete = models.BooleanField("删除", default=False)
    create_time = models.DateTimeField("更新时间", auto_now_add=True)
    update_time = models.DateTimeField("创建时间", auto_now=True)

    def __str__(self) -> str:
        return self.name

class Cases(models.Model):
    """
    用例表
    """
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    name = models.CharField("名称", max_length=100, mull=False, default="")
    priority = models.CharField("优先级", max_length=20, null=False, default="")
    conditionsPre = models.TextField("前置条件", default="")
    
    create_time = models.DateTimeField("更新时间", auto_now_add=True)
    update_time = models.DateTimeField("创建时间", auto_now=True)
