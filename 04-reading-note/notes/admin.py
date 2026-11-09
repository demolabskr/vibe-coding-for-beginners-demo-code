from django.contrib import admin

from .models import AICall, Book, Note


class NoteInline(admin.TabularInline):
    model = Note
    extra = 1


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "owner", "status", "rating", "finished_on"]
    list_filter = ["status"]
    search_fields = ["title", "author"]
    inlines = [NoteInline]


@admin.register(AICall)
class AICallAdmin(admin.ModelAdmin):
    list_display = ["created_at", "user", "feature", "status", "seconds", "error"]
    list_filter = ["feature", "status"]


admin.site.site_header = "나의 독서 노트 관리"
