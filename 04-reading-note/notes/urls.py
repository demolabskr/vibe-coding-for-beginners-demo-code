from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("books/<int:pk>/", views.book_detail, name="book_detail"),
    path("about/", views.about, name="about"),
]
