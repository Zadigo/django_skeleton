import inspect
from collections import defaultdict
from importlib import import_module


class AppConfig:
    def __init__(self, name, module):
        self.apps = None
        self.name = name
        self.app_module = module
        
        if not hasattr(self, 'label'):
            self.label = name
                    
        if not hasattr(self, 'verbose_name'):
            self.verbose_name = name.title()
            
        self.path = self.get_path_from_module(module)
        
        self.models_module = None
        self.models = []
        
    def __repr__(self):
        return f'<{self.__class__.__name__}(app={self.label})>'

    @classmethod
    def create(cls, name):
        try:
            app_module = import_module(name)
        except:
            raise
        else:
            apps_submodule_path = f'{name}.apps'
            apps_submodule = import_module(apps_submodule_path)
            
            candidates = [(name, klass) for name, klass in inspect.getmembers(apps_submodule, inspect.isclass) if issubclass(klass, cls) and klass != cls]
            
            if len(candidates) == 1:
                app_config_class = candidates[0][1]
                
            try:
                # Reload the module using the name registered
                # in the AppConfig class of the app to make
                # sure that the module exists
                app_module = import_module(app_config_class.name)
            except:
                raise
                
        return app_config_class(name, app_module)
    
    @staticmethod
    def get_path_from_module(module):
        paths = getattr(module, '__path__')
        return paths[0]

    def import_models(self):
        self.models = apps.all_models[self.label]
        # import_submodule function
        models_module_path = f'{self.name}.models'
        self.models_module = import_module(models_module_path)
            
    def ready(self):
        pass


class Apps:
    def __init__(self, installed_apps=None):
        self.app_configs = {}
        self.all_models = defaultdict(dict)
        self.apps_ready = False
        self.models_ready = False

    def populate(self, apps):
        for app in apps:
            instance = AppConfig.create(app)
            self.app_configs[instance.label] = instance
            instance.apps = self
            
        for app in self.app_configs.values():
            app.import_models()
            
        self.models_ready = True

        for app in self.app_configs.values():
            app.ready()
            
        self.apps_ready = True
            
    def get_app_config(self, name) -> AppConfig:
        candidates = []
        
        module_name = name.rsplit('.', maxsplit=1)[0]
        for instance in self.app_configs.values():
            if instance.name.startswith(module_name):
                candidates.append(instance)
        
        if candidates:
            return sorted(candidates, key=lambda candidate: -len(candidate.name))[0]

    def register_model(self, app_label, model):
        model_name = model._meta.model_name
        app_models = self.all_models[app_label]
        if model_name in app_models:
            pass
        app_models[model_name] = model

apps = Apps(installed_apps=None)
