from importlib import import_module

class BaseDatabaseOperations:
    compiler_module = 'django_structure.db.models.sql.compiler'
    
    def __init__(self, connection):
        self.connection = connection
        self._cache = None

    def compiler(self, compiler_name):
        if self._cache is None:
            self._cache = import_module(self.compiler_module)
        return getattr(self._cache, compiler_name)
