def setup():
    from django_skeleton.apps import apps
    from django_skeleton.settings import settings
    
    apps.populate(settings.INSTALLED_APPS)
