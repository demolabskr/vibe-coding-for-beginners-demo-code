"""파이썬 앱(03-python-apps/book_cli/books.db)의 책을 웹앱 데이터베이스로 옮긴다.

먼저 몇 권이 옮겨질지 보여 주고, --apply를 붙였을 때만 실제로 옮긴다.
    uv run python manage.py import_books
    uv run python manage.py import_books --apply
"""
import sqlite3

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from notes.models import Book

SOURCE = settings.BASE_DIR.parent / "03-python-apps" / "book_cli" / "books.db"
STATUS_MAP = {"읽고 싶음": Book.Status.WANT, "읽는 중": Book.Status.READING, "다 읽음": Book.Status.DONE}


class Command(BaseCommand):
    help = "books.db의 책을 웹앱으로 옮긴다(같은 제목과 저자는 건너뜀)."

    def add_arguments(self, parser):
        parser.add_argument("--apply", action="store_true", help="실제로 옮긴다")

    def handle(self, *args, **options):
        if not SOURCE.exists():
            raise CommandError(f"{SOURCE} 파일이 없습니다.")
        with sqlite3.connect(SOURCE) as conn:
            rows = conn.execute("SELECT title, author, status FROM books").fetchall()

        new_rows = [r for r in rows if not Book.objects.filter(title=r[0], author=r[1]).exists()]
        self.stdout.write(f"books.db {len(rows)}권 가운데 새로 옮길 책 {len(new_rows)}권")
        for title, author, status in new_rows:
            self.stdout.write(f"  - {title} / {author} [{status}]")
        if not options["apply"]:
            self.stdout.write("미리보기입니다. 옮기려면 --apply를 붙여 다시 실행하세요.")
            return
        for title, author, status in new_rows:
            Book.objects.create(title=title, author=author, status=STATUS_MAP.get(status, Book.Status.WANT))
        self.stdout.write(self.style.SUCCESS(f"{len(new_rows)}권을 옮겼습니다."))
