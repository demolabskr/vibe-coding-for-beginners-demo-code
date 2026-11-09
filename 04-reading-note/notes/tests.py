"""나의 독서 노트의 주요 기능 테스트.

실행: uv run python manage.py test
AI 기능은 Codex를 실제로 부르지 않고 가짜 답으로 바꿔 시험한다(시간, 사용량, 결과가 매번 다른 문제를 피한다).
"""
import json
from datetime import date, timedelta
from unittest import mock

from django.contrib.auth.models import User
from django.test import TestCase, override_settings

from .ai import AIError
from .models import AICall, Book, Note


class BookTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("haneul", password="pass-for-test-1")
        self.other = User.objects.create_user("minsu", password="pass-for-test-2")
        self.client.login(username="haneul", password="pass-for-test-1")
        self.book = Book.objects.create(owner=self.user, title="아몬드", author="손원평")


class LoginAndOwnerTests(BookTestCase):
    def test_login_required(self):
        self.client.logout()
        response = self.client.get("/books/new/")
        self.assertRedirects(response, "/accounts/login/?next=/books/new/")

    def test_cannot_open_other_users_book(self):
        theirs = Book.objects.create(owner=self.other, title="남의 책")
        self.assertEqual(self.client.get(f"/books/{theirs.pk}/").status_code, 404)
        self.assertEqual(self.client.post(f"/books/{theirs.pk}/delete/").status_code, 404)
        self.assertTrue(Book.objects.filter(pk=theirs.pk).exists())

    def test_list_shows_only_my_books(self):
        Book.objects.create(owner=self.other, title="남의 책")
        response = self.client.get("/")
        self.assertContains(response, "아몬드")
        self.assertNotContains(response, "남의 책")


class BookFormTests(BookTestCase):
    def test_create_book(self):
        response = self.client.post("/books/new/", {"title": "데미안", "author": "헤르만 헤세", "status": "want"})
        self.assertRedirects(response, "/")
        self.assertEqual(Book.objects.get(title="데미안").owner, self.user)

    def test_future_finished_date_is_rejected(self):
        tomorrow = (date.today() + timedelta(days=1)).isoformat()
        response = self.client.post(
            "/books/new/", {"title": "미래의 책", "status": "done", "finished_on": tomorrow}
        )
        self.assertContains(response, "오늘보다 뒤일 수 없습니다")
        self.assertFalse(Book.objects.filter(title="미래의 책").exists())

    def test_delete_needs_post(self):
        self.client.get(f"/books/{self.book.pk}/delete/")
        self.assertTrue(Book.objects.filter(pk=self.book.pk).exists())
        self.client.post(f"/books/{self.book.pk}/delete/")
        self.assertFalse(Book.objects.filter(pk=self.book.pk).exists())


class SearchTests(BookTestCase):
    def test_search_by_part_of_title(self):
        Book.objects.create(owner=self.user, title="채식주의자", author="한강")
        response = self.client.get("/", {"q": "채식"})
        self.assertContains(response, "채식주의자")
        self.assertNotContains(response, "아몬드")


class AITests(BookTestCase):
    def setUp(self):
        super().setUp()
        Note.objects.create(book=self.book, body="마음이 따뜻해졌다.")

    @mock.patch("notes.ai_views.ask_codex", return_value="- 마음이 따뜻해졌다.")
    def test_summary_is_saved_and_marked_as_ai(self, fake_ask):
        self.client.post(f"/books/{self.book.pk}/ai/summary/")
        self.book.refresh_from_db()
        self.assertEqual(self.book.summary, "- 마음이 따뜻해졌다.")
        self.assertTrue(self.book.summary_by_ai)
        self.assertEqual(AICall.objects.get().status, AICall.Status.OK)

    @mock.patch("notes.ai_views.ask_codex", return_value=json.dumps({"tags": ["소설", "없는태그"]}))
    def test_unknown_tags_are_dropped(self, fake_ask):
        self.client.post(f"/books/{self.book.pk}/ai/tags/")
        self.book.refresh_from_db()
        self.assertEqual(self.book.tags, "소설")

    @mock.patch("notes.ai_views.ask_codex", side_effect=AIError("Codex 로그인이 풀렸습니다."))
    def test_error_is_shown_and_recorded(self, fake_ask):
        response = self.client.post(f"/books/{self.book.pk}/ai/summary/", follow=True)
        self.assertContains(response, "Codex 로그인이 풀렸습니다.")
        self.assertEqual(AICall.objects.get().status, AICall.Status.ERROR)

    @override_settings(AI_DAILY_LIMIT=1)
    @mock.patch("notes.ai_views.ask_codex", return_value="- 요약")
    def test_daily_limit(self, fake_ask):
        self.client.post(f"/books/{self.book.pk}/ai/summary/")
        response = self.client.post(f"/books/{self.book.pk}/ai/summary/", follow=True)
        self.assertContains(response, "모두 썼습니다")
        self.assertEqual(fake_ask.call_count, 1)

    def test_codex_not_found(self):
        with mock.patch("notes.ai.shutil.which", return_value=None):
            response = self.client.post(f"/books/{self.book.pk}/ai/summary/", follow=True)
        self.assertContains(response, "codex 명령을 찾을 수 없습니다")
