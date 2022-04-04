from django_structure.settings import settings
from django_structure.setup import setup

settings.configure(INSTALLED_APPPS=['test_app'])

setup()

from django_structure.apps import apps
from test_app.models import Book

print(vars(apps))
print(Book.objects)

queryset = Book.objects.all()
print(queryset)
