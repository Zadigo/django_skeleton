

class BaseTable:
    def __init__(self, table_name, table_alias):
        self.table_name = table_name
        self.table_alias = table_alias
        
    def as_sql(self, compiler, connection):
        alias_string = ''
        base_sql = compiler.quote_name_unless_alias(self.table_name)
        return base_sql + alias_string, []
