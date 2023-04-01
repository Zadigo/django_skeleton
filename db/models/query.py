from django_skeleton.db.models.sql.query import Query


class BaseIterable:
    def __init__(self, queryset, chunk_size=100):
        self.queryset = queryset
        self.chunk_size = chunk_size


class ModelIterable(BaseIterable):
    def __iter__(self):
        queryset = self.queryset
        db = queryset.db # default
        compiler = queryset.query.get_compiler(using=db)
        # This is the section where the compiler
        # actually gets executed
        results = compiler.execute_sql(True, chunk_size=self.chunk_size)
        selected_columns, klass_info, annotation_col_map = (
            compiler.select,
            compiler.klass_info,
            compiler.annotation_col_map
        )
        
        model_cls = klass_info['model']
        select_fields = klass_info['select_fields']
        column_names_list = [
            f[0].target.attname
                for f in select_fields[model_fields_start:model_fields_end]
        ]
        model_fields_start, model_fields_end = select_fields[0], select_fields[-1] + 1
        for row in compiler.result_iter(results):
            obj = model_cls.from_db(db, column_names_list, row[model_fields_start:model_fields_end])
            yield obj
            

class QuerySet:
    def __init__(self, model=None, query=None, using=None, hints=None):
        self.model = model
        self._result_cache = None
        self._query = query or Query(self.model)
        self._iterable_class = ModelIterable
        self._db = using
        self._hints = hints
    
    def __repr__(self):
        data = list(self)
        return f'<{self.__class__.__name__} {data}>'
    
    def __iter__(self):
        self._fetch_all()
        return iter(self._result_cache)
        
    def __len__(self):
        self._fetch_all()
        return len(self._result_cache)
    
    @property
    def db(self):
        # NOTE: In django, this uses some
        # sort of router.db_for_read
        return self._db or 'default'
    
    @property
    def query(self):
        return self._query
    
    def _fetch_all(self):
        if self._result_cache is None:
            self._result_cache = list(self._iterable_class(self))

    def count(self):
        return self._query.get_count()
    
    def get(self, *args, **kwargs):
        return 'Get!'
    
    def filter(self, *args, **kwargs):
        return 'Filtered!'
