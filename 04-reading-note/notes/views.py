from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q
from django.db.models.functions import ExtractMonth
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import BookForm, NoteForm, SignUpForm
from .models import Book

SORTS = {"new": "-created_at", "rating": "-rating", "title": "title"}


def my_book(request, pk):
    """로그인한 사람의 책만 꺼낸다. 다른 사람의 책 번호면 404."""
    return get_object_or_404(Book, pk=pk, owner=request.user)


@login_required
def home(request):
    books = Book.objects.filter(owner=request.user)
    q = request.GET.get("q", "").strip()
    status = request.GET.get("status", "")
    sort = request.GET.get("sort", "new")
    if q:
        books = books.filter(Q(title__icontains=q) | Q(author__icontains=q))
    if status in Book.Status.values:
        books = books.filter(status=status)
    books = books.order_by(SORTS.get(sort, "-created_at"), "-created_at")
    page = Paginator(books, 10).get_page(request.GET.get("page"))
    return render(request, "notes/home.html", {
        "page": page, "q": q, "status": status, "sort": sort, "statuses": Book.Status.choices,
    })


@login_required
def book_detail(request, pk):
    book = my_book(request, pk)
    return render(request, "notes/book_detail.html", {"book": book, "note_form": NoteForm()})


@login_required
def book_create(request):
    form = BookForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        book = form.save(commit=False)
        book.owner = request.user
        book.save()
        messages.success(request, f"'{book.title}'을(를) 등록했습니다.")
        return redirect("home")
    return render(request, "notes/book_form.html", {"form": form, "heading": "책 등록"})


@login_required
def book_update(request, pk):
    book = my_book(request, pk)
    form = BookForm(request.POST or None, request.FILES or None, instance=book)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "책 정보를 고쳤습니다.")
        return redirect("book_detail", pk=book.pk)
    return render(request, "notes/book_form.html", {"form": form, "heading": "책 정보 고치기", "book": book})


@login_required
def book_delete(request, pk):
    book = my_book(request, pk)
    if request.method == "POST":
        title = book.title
        book.delete()
        messages.success(request, f"'{title}'을(를) 지웠습니다.")
        return redirect("home")
    return render(request, "notes/book_confirm_delete.html", {"book": book})


@login_required
def note_add(request, pk):
    book = my_book(request, pk)
    form = NoteForm(request.POST)
    if request.method == "POST" and form.is_valid():
        note = form.save(commit=False)
        note.book = book
        note.save()
        messages.success(request, "메모를 남겼습니다.")
    return redirect("book_detail", pk=book.pk)


@login_required
def stats(request):
    year = timezone.localdate().year
    mine = Book.objects.filter(owner=request.user)
    done_this_year = mine.filter(status=Book.Status.DONE, finished_on__year=year)
    by_month = dict(
        done_this_year.annotate(month=ExtractMonth("finished_on")).values_list("month").annotate(n=Count("id"))
    )
    months = [{"month": m, "count": by_month.get(m, 0)} for m in range(1, 13)]
    top = max([m["count"] for m in months] + [1])
    for m in months:
        m["percent"] = round(m["count"] / top * 100)
    return render(request, "notes/stats.html", {
        "year": year,
        "done_count": done_this_year.count(),
        "months": months,
        "average": mine.filter(rating__isnull=False).aggregate(avg=Avg("rating"))["avg"],
        "by_status": [(label, mine.filter(status=value).count()) for value, label in Book.Status.choices],
    })


def signup(request):
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "가입을 마쳤습니다. 첫 책을 등록해 보세요.")
        return redirect("home")
    return render(request, "registration/signup.html", {"form": form})


def about(request):
    return render(request, "notes/about.html")
