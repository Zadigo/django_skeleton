def setup():
    from django_structure.apps import apps
    from django_structure.settings import settings
    apps.populate(settings.INSTALLED_APPS)
