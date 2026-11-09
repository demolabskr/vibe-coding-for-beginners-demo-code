from django.urls import path

from . import ai_views, views

urlpatterns = [
    path("", views.home, name="home"),
    path("books/new/", views.book_create, name="book_create"),
    path("books/<int:pk>/", views.book_detail, name="book_detail"),
    path("books/<int:pk>/edit/", views.book_update, name="book_update"),
    path("books/<int:pk>/delete/", views.book_delete, name="book_delete"),
    path("books/<int:pk>/notes/add/", views.note_add, name="note_add"),
    path("books/<int:pk>/ai/summary/", ai_views.summarize, name="ai_summary"),
    path("books/<int:pk>/ai/tags/", ai_views.tag, name="ai_tags"),
    path("books/<int:pk>/ai/edit/", ai_views.edit_ai, name="ai_edit"),
    path("recommend/", ai_views.recommend, name="recommend"),
    path("stats/", views.stats, name="stats"),
    path("signup/", views.signup, name="signup"),
    path("about/", views.about, name="about"),
]
