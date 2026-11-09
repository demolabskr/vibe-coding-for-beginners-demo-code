from django.urls import path

from . import views

urlpatterns = [
    path("", views.entry_list, name="entry_list"),
    path("report/", views.weekly_report, name="weekly_report"),
]
