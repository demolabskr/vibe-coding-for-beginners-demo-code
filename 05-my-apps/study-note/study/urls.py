from django.urls import path

from . import views

urlpatterns = [
    path("", views.note_list, name="note_list"),
    path("notes/<int:pk>/", views.note_detail, name="note_detail"),
    path("notes/<int:pk>/quiz/make/", views.make_quiz, name="make_quiz"),
    path("notes/<int:pk>/quiz/", views.solve, name="solve"),
    path("review/", views.review, name="review"),
]
