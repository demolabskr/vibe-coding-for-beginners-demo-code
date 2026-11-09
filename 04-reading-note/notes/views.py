from django.shortcuts import get_object_or_404, render

from .models import Book


def home(request):
    books = Book.objects.all()
    return render(request, "notes/home.html", {"books": books})


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, "notes/book_detail.html", {"book": book})


def about(request):
    return render(request, "notes/about.html")
