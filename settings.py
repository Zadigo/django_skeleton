import os
import global_settings
from django_skeleton.utils import LazyObject

class UserSettings:
    def __init__(self, default_settings):
        pass


class Settings:
    # NOTE: We should get INSTALLED_APPS
    # from the user settings
    INSTALLED_APPS = ['test_app']
    
    def __init__(self, dotted_path):
        pass
    
    def configure(self, **kwargs):
        user_settings = UserSettings(global_settings)

    
class LazySettings(LazyObject):
    def _setup(self):
        # NOTE: This is None. Should get the project settings
        # but since this a mockup we'll simulate this
        project_settings_path = os.environ.get('MY_SETTINGS')
        self.container = Settings(project_settings_path)


settings = LazySettings()
