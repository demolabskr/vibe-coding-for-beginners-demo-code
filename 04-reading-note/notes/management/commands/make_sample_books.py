"""페이지 나누기 실습용 가짜 책을 만든다.

    uv run python manage.py make_sample_books 사용자이름 [--count 50]
"""
import random
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from notes.models import Book

WORDS = ["바다", "도시", "고양이", "여름", "편지", "기억", "정원", "별", "기차", "숲", "겨울", "골목"]


class Command(BaseCommand):
    help = "실습용 가짜 책을 만든다(제목 앞에 [예시]가 붙는다)."

    def add_arguments(self, parser):
        parser.add_argument("username")
        parser.add_argument("--count", type=int, default=50)

    def handle(self, *args, **options):
        user = get_user_model().objects.filter(username=options["username"]).first()
        if user is None:
            raise CommandError(f"사용자 {options['username']}이(가) 없습니다.")
        today = date.today()
        for n in range(1, options["count"] + 1):
            status = random.choice(Book.Status.values)
            done = status == Book.Status.DONE
            Book.objects.create(
                owner=user,
                title=f"[예시] {random.choice(WORDS)}의 {random.choice(WORDS)} {n}",
                author=f"가상 작가 {random.randint(1, 20)}",
                status=status,
                rating=random.randint(1, 5) if done else None,
                finished_on=today - timedelta(days=random.randint(0, 300)) if done else None,
            )
        self.stdout.write(self.style.SUCCESS(f"가짜 책 {options['count']}권을 만들었습니다."))
