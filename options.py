import bisect
from functools import cached_property

from django_structure.apps import apps

DEFAULT_NAMES = {'verbose_name'}

class Options:
    default_apps = apps

    def __init__(self, meta, app_label=None):
        self.pk = None
        self.apps = self.default_apps
        self.app_label = app_label
        self.meta = meta
        self.private_fields = []
        self.local_many_to_many = []
        self.local_fields = []
        self.model = None
        self.model_name = None
        self.local_managers = []
        self.managers = []
        
    def __repr__(self):
        return f'<{self.__class__.__name__} for {self.model_name}>'
    
    @cached_property
    def managers_map(self):
        return {manager.name: manager for manager in self.managers}
        
    def _prepare(self, cls):
        pass

    def contribute_to_class(self, cls, name):
        # FIXME: The cls that comes here is
        # extremely confusing as of what class
        # exactly is being used here
        cls._meta = self
        self.model = cls

        # TODO: What name of the object to use
        # because when we call __name__ on the
        # class, it gives the field name and
        # __class__.__name__ gives the BaseModel
        # (since the model is not instanciated)
        self.object_name = cls.__name__
        self.model_name = self.object_name.lower()

        if self.meta is not None:
            attrs = self.meta.__dict__.copy()

    def add_field(self, field, private=False):
        if private:
            self.private_fields.append(field)
        elif field.is_relation or field.many_to_many:
            bisect.insort(self.local_many_to_many, field)
        else:
            bisect.insort(self.local_fields, field)
            self.set_primary_key(field)
            
    def add_manager(self, manager):
        # self.local_managers.append(manager)
        self.managers.append(manager)
            
    def set_primary_key(self, field):
        if self.pk is None and field.is_primary_key:
            self.pk = field
            field.serialze = False
