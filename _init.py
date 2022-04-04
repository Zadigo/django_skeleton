from django_structure.settings import settings
from django_structure.setup import setup

settings.configure(INSTALLED_APPPS=['test_module'])

setup()

from django_structure.apps import apps
from test_module.models import Book

queryset = Book.objects.all()
print(vars(apps))
print(queryset)
