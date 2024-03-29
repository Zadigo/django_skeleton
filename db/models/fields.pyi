from functools import cached_property, total_ordering
from typing import Any, Tuple

from django_skeleton.db.models.expressions import Col

@total_ordering
class Field:
    is_relation: bool = ...
    is_primary_key: bool = ...
    db_column: str = ...
    many_to_many: bool = ...
    model: str = ...
    name: str = ...
    verbose_name: str = ...

    def __init__(self, **kwargs) -> None: ...
    def __eq__(self, value: Any) -> bool: ...
    def __gt__(self, value: Any) -> bool: ...
    @cached_property
    def cached_col(self) -> Col: ...
    def contribute_to_class(self, cls, name) -> None: ...
    def get_attname(self) -> str: ...
    def get_attname_column(self) -> Tuple[str, str]: ...
    def get_col(self, alias: str, output_field: Field = None) -> Col: ...


class CharField(Field):
    ...
