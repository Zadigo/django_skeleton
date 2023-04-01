from django_skeleton.apps import apps
from django_skeleton.db.models.managers import Manager
from django_skeleton.db.models.options import Options


class BaseModel(type):
    def __new__(cls, name, bases, attrs):
        super_new = super().__new__
        
        parents  = [base for base in bases if isinstance(base, BaseModel)]
        if not parents:
            return super_new(cls, name, bases, attrs)
        
        module = attrs['__module__']
        classcell = attrs.get('__classcell__', None)
        new_attrs = {
            '__module__': module,
            '__qualname__': attrs['__qualname__']
        }
        if classcell is not None:
            new_attrs['__classcell__'] = classcell
        
        elements = {}
        for item_name, item in attrs.items():
            if hasattr(item, 'contribute_to_class'):
                elements[item_name] = item
            else:
                new_attrs[item_name] = item
        
        new_class = super_new(cls, name, bases, new_attrs)
        
        meta_attributes_class = attrs.get('Meta', getattr(new_class, 'meta', None))
        
        app_label = None
        app_config = apps.get_app_config(module)
        # app_label = app_config.label
        app_label = app_config.name
        # TODO: The app_label is more Options for a given model
        options = Options(meta_attributes_class, app_label=app_label)
        new_class.add_to_class('_meta', options)
        
        for element_name, element in elements.items():
            new_class.add_to_class(element_name, element)
        
        new_class._prepare()
        new_class._meta.apps.register_model(new_class._meta.app_label, new_class)
        
        return new_class
    
    @property
    def _base_manager(cls):
        return cls._meta.base_manager
    
    @property
    def _default_manager(cls):
        return cls._meta.default_manager

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = cls(*values)
        return instance

    def _prepare(cls):
        options = cls._meta
        options._prepare(cls)
        
        if not options.managers:
            manager = Manager()
            manager.auto_created = True
            cls.add_to_class('objects', manager)
        
        if cls.__doc__ is None:
            cls.__doc__ = 'Auto created model'
            
    def add_to_class(cls, name, value):
        if hasattr(value, 'contribute_to_class'):
            value.contribute_to_class(cls, name)
        else:
            setattr(cls, name, value)


class Model(metaclass=BaseModel):
    def __init__(self, *args, **kwargs):
        pass
    
    def __repr__(self):
        return f'<{self.__class__.__name__}: {self}>'

    def __str__(self) :
        return f'{self.__class__.__name__} object {self.pk}'
