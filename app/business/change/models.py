# pyright: reportIncompatibleVariableOverride=false
"""
change — 业务模型定义。

在此文件中定义 Tortoise ORM 模型，完成后运行:

    just cli-crud change

即可一次生成后端 schemas / controllers / api 及前端 service / views / i18n 等文件。
"""

from tortoise import fields

from app.utils import AuditMixin, BaseModel, StatusType


class ChangeRequest(BaseModel, AuditMixin):
    """变更需求"""

    id = fields.IntField(primary_key=True)
    request_no = fields.CharField(max_length=50, description="需求编号")
    requester = fields.CharField(max_length=50, description="需求提出人")
    department = fields.CharField(max_length=100, description="所在部门")
    request_date = fields.DateField(description="提出日期")
    location = fields.CharField(max_length=200, description="变更地点/位置")
    source = fields.CharField(max_length=50, description="需求来源")
    description = fields.TextField(description="变更需求描述")
    background = fields.TextField(null=True, description="需求背景与目的")
    status = fields.CharEnumField(enum_type=StatusType, default=StatusType.enable, description="状态")

    class Meta:
        table = "biz_change_request"
        table_description = "变更需求"