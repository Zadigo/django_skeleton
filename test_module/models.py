from django_structure.models import Model
from django_structure import fields


class Book(Model):
    surname = fields.CharField()
