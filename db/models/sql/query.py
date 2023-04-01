from django_skeleton.db import connections
from django_skeleton.db.models.sql.datastructures import BaseTable
from django_skeleton.db.utils import DEFAULT_DB_ALIAS


class BaseExpression:
    def __init__(self, output_field=None):
        pass


class Query(BaseExpression):
    compiler = 'SQLCompiler'

    def __init__(self, model):
        self.model = model
        self.table_map = {}
        self.alias_refcount = {}

    def __str__(self):
        sql, params = self.sql_with_params()
        return sql % params

    def clone(self):
        obj = type(self.__class__.__name__, (), self.__dict__.copy())
        obj.__class__ = self.__class__
        return obj

    def sql_with_params(self):
        return self.get_compiler(DEFAULT_DB_ALIAS).as_sql()

    def get_compiler(self, using=None, connection=None):
        # NOTE: using here is "default" which
        # is the default value in DATABASE in
        # the settings file
        if using is None and connection is None:
            raise ValueError("No default database to connect to")

        if using:
            connection = connections[using]

        # TODO: Check this workflow
        return connection.database_operations.compiler(self.compiler)(self, connection, using)

    def get_count(self):
        # NOTE: The methods in these technically
        # return SQL bits of strings that will
        # be joined to create the final string
        cloned_query = self.clone()
        return f"Counted: {len([1, 2])}"

    def table_alias(self, table_name, create=False):
        alias_list = self.table_map.get(table_name)
        if not alias_list:
            self.table_map[table_name] = [table_name]
        self.alias_map[table_name] = table_name
        self.alias_refcount[table_name] = 1
        return table_name, True

    def join(self, table):
        alias, _ = self.table_alias(table.table_name, create=True)
        table.table_alias = alias
        self.alias_map[alias] = table
        return alias

    def join_parent_model(self, model_options, model, alias, seen_models):
        if model in seen_models:
            return seen_models[model]

    def get_initial_alias(self):
        table_name = self.model._meta.db_table
        table = BaseTable(table_name, None)
        alias = self.join(table.table_name)
        return alias
