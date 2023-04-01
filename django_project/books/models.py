from django.db import models
from django.urls import reverse


class Book(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('books:book', kwargs={'pk': self.pk})
