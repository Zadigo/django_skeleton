import os
import global_settings
from django_structure.utils import LazyObject 

class UserSettings:
    def __init__(self, default_settings):
        pass


class Settings:
    INSTALLED_APPS = ['test_module']
    
    def __init__(self, dotted_path):
        pass
    
    def configure(self, **kwargs):
        user_settings = UserSettings(global_settings)

    
class LazySettings(LazyObject):
    def _setup(self):
        project_settings_path = os.environ.get('MY_SETTINGS')
        self.container = Settings(project_settings_path)


settings = LazySettings()
