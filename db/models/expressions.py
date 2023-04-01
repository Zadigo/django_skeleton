class BaseExpression:
    def __init__(self, output_field=None):
        if output_field is not None:
            self.output_field = output_field


class Expression(BaseExpression):
    pass


class Col(Expression):
    contains_column_references = True
    possibly_multivalued = False

    def __init__(self, alias, target, output_field=None):
        if output_field is None:
            output_field = target
        super().__init__(output_field=output_field)
        self.alias = alias
        self.target = target
        
    def as_sql(self, compiler, connection):
        alias = self.alias
        column = self.target.column
        identifiers = (alias, column) if alias else (column,)
        sql = '.'.join(map(compiler.quote_name_unless_alias, identifiers))
        return sql, []

    def select_format(self, compiler, sql, params):
        if hasattr(self.output_field, 'select_format'):
            return self.output_field.select_format(compiler, sql, params)
        return sql, params
