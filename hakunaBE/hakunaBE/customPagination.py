from typing import Any, List
from ninja.pagination import PaginationBase
from ninja import Schema, Field
from ninja.types import DictStrAny
from django.db.models import QuerySet
from ninja.conf import settings


class CustomPagination(PaginationBase):
    """
    自定义分页器
    """
    class Input(Schema):
        page: int = Field(1, gt=0)

    def __init__(self, page_size: int = settings.PAGINATION_PER_PAGE, **kwargs: Any) -> None:
        self.page_size = page_size
        super().__init__(**kwargs)

    class Output(Schema):
        items: List[Any]
        page: int
        total: int
        per_page: int

    def paginate_queryset(
        self, queryset: QuerySet, pagination: Input, **params: DictStrAny
    ) -> QuerySet:
        page: int = pagination.page  # type: ignore
        offset = (page - 1) * self.page_size
        data = {
            "items": queryset[offset: offset + self.page_size],
            "page": page,
            "per_page": self.page_size,
            "total": len(queryset),
        }
        return data
