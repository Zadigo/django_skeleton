from books import views
from django.urls import re_path

app_name = 'books'

urlpatterns = [
    re_path(r'^book/(?P<pk>\d+)$', views.book, name='book'),
    re_path(r'^$', views.books, name='books')
]
