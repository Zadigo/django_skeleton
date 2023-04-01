from django.shortcuts import render
from books.models import Book


def books(request, **kwargs):
    books = Book.objects.all()
    return render(request, 'books.html', context={'books': books})


def book(request, pk, **kwargs):
    book = Book.objects.get(id=pk)
    return render(request, 'book.html', context={'book': book})
