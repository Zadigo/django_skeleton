from django_skeleton.db.models.models import Model
from db.models import fields


class Book(Model):
    surname = fields.CharField()

print(Book.objects.all())
