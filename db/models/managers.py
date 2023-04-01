import inspect

from django_skeleton.db.models.query import QuerySet


class BaseManager:
    auto_created = False
    
    def __init__(self):
        self.name = None
        self.model = None
        self._db = None
        # self.managers = []
        # self.base_manager = None
        # self.default_manager = None

    def __repr__(self):
        return f'{self.model._meta.app_label}.{self.name}'
    
    @classmethod
    def from_queryset(cls, queryset_class, class_name=None):
        if class_name is None:
            class_name = f'{cls.__class__.__name__}From{queryset_class.__name__}'
        # NOTE: _queryset_class is implemented here and
        # returns a new BaseManager the QuerySet
        attrs = {
            '_queryset_class': queryset_class,
            **cls.get_queryset_methods(queryset_class)
        }
        return type(class_name, (cls,), attrs)

    @classmethod
    def get_queryset_methods(cls, queryset_class):
        def create_method(name, method):
            def manager_method(self, *args, **kwargs):
                return getattr(self.get_queryset(), name)(*args, **kwargs)
            manager_method.__name__ = method.__name__
            manager_method.__doc__ = method.__doc__
            return manager_method
        
        methods = {}
        for name, method in inspect.getmembers(queryset_class, inspect.isfunction):
            if hasattr(cls, name):
                continue
            
            if name.startswith('__'):
                continue
            
            methods[name] = create_method(name, method)
        return methods
            
    def contribute_to_class(self, cls, name):
        self.name = self.name or name
        self.model = cls
        # This sets the objects attribute here
        # on the cls model class / name = 'objects'
        setattr(cls, name, ManagerDescriptor(self))
        cls._meta.add_manager(self)

    def get_queryset(self):
        # NOTE: This returns a new custom queryset
        # instance when methods are called on the
        # Manager. Method all() does the same
        return self._queryset_class(model=self.model, using=self._db)

    def all(self):
        return self.get_queryset()


# NOTE: Since we want to create a custom manager
# for each model, this technique creates a fresh
# new manager from the QuerySet class
# NOTE: This technique does not implement the
# methods of the QuuerySet class so they have
# to be reimplemented
class Manager(BaseManager.from_queryset(QuerySet)):
    pass


# NOTE: The descriptor implements on the
# 'objects' attribute on the Manager and
# implements also how it can/should be
# accessed
class ManagerDescriptor:
    def __init__(self, manager):
        self.manager = manager

    def __get__(self, instance, cls=None):
        return cls._meta.managers_map[self.manager.name]
