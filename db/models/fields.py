from functools import cached_property, total_ordering


@total_ordering
class Field:
    def __init__(self, **kwargs):
        self.name = None
        self.db_column = None
        self.verbose_name = None
        self.many_to_many = False
        self.is_relation = False
        self.is_primary_key = False
        self.model = None
        
    def __eq__(self, value):
        return True
        
    def __gt__(self, value):
        return True
    
    @cached_property
    def cached_col(self):
        from django_structure.db.models.expressions import Col
        return Col(self.model._meta.db_table, self)
        
    def contribute_to_class(self, cls, name):
        self.name = name
        self.attname, self.column = self.get_attname_column()
        self.verbose_name = name.replace('_', ' ')
        self.model = cls
        cls._meta.add_field(self)
        
    def get_attname(self):
        return self.name
    
    def get_attname_column(self):
        attname = self.get_attname()
        return attname, self.db_column or attname
    
    def get_col(self, alias, output_field=None):
        if alias == self.model._meta.db_table and (output_field is None or output_field == self):
            return self.cached_col
        from django_structure.db.models.expressions import Col
        return Col(self.model._meta.db_table, self)

    def select_format(self, compiler, sql, params):
        return sql, params


class CharField(Field):
    pass
