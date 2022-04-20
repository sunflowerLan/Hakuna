
from django.db import models
from module.models import Module

# Create your models here.

class TestCase(models.Model):
    """
    用例表
    """
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    name = models.CharField("名称", max_length=100, null=False, default="")
    method = models.CharField("请求方法", max_length=10, null=False)
    url = models.TextField("URL", null=False)
    header = models.TextField("请求头", null=True, default="{}")
    params_type = models.CharField("参数类型", max_length=10, null=False)
    params_body = models.TextField("参数内容", null=True, default="{}")
    result = models.TextField("响应", null=True, default="{}")
    assert_type = models.CharField("断言类型", max_length=10, null=True)
    assert_text = models.TextField("断言结果", null=True, default="{}")
    is_delete = models.BooleanField("状态", default=False)
    # priority = models.CharField("优先级", max_length=20, null=False, default="")
    # conditionsPre = models.TextField("前置条件", default="{}")
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    def __str__(self) -> str:
        return self.name