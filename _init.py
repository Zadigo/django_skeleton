from django_skeleton.settings import settings
from django_skeleton.setup import setup

settings.configure(INSTALLED_APPPS=['test_app'])

setup()

from django_skeleton.apps import apps
from test_app.models import Book
# from django_skeleton.query import QuerySet
# print(vars(apps))
# print(Book.objects)

# queryset = Book.objects.all()
# print(queryset)
total = Book.objects.all()
print(total)
