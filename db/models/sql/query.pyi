from typing import Literal, Optional, Tuple

from django_skeleton.db.models.fields import Field
from django_skeleton.db.models.models import Model
from django_skeleton.db.models.sql.compiler import SQLCompiler
from django_skeleton.db.models.sql.datastructures import BaseTable
from django_skeleton.db.utils import BaseConnectionHandler


class BaseExpression:
    def __init__(self, output_field: Optional[Field] = ...): ...


class Query(BaseExpression):
    compiler: Literal['SQLCompiler'] = ...

    def __init__(self, model: Model): ...
    def __str__(self) -> str: ...
    def clone(self) -> Query: ...
    def sql_with_params(self) -> str: ...
    def get_compiler(self, using: Optional[str] = ..., connection: Optional[BaseConnectionHandler] = ...) -> SQLCompiler: ...
    def get_count(self) -> int: ...
    def join(self, table: BaseTable) -> str: ...
    def table_alias(self, table_name: str, create: Optional[bool] = ...) -> Tuple[str, True]: ...
    def get_initial_alias(self) -> str: ...
