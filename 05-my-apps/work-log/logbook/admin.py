from django.contrib import admin

from .models import Entry, WeeklyReport

admin.site.register(Entry)
admin.site.register(WeeklyReport)
