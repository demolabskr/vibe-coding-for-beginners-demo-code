from django.conf import settings
from django.db import models
from django.utils import timezone


class Book(models.Model):
    """책 한 권. docs/data-design.md의 책 표와 같다."""

    class Status(models.TextChoices):
        WANT = "want", "읽고 싶음"
        READING = "reading", "읽는 중"
        DONE = "done", "다 읽음"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="books", verbose_name="주인"
    )
    title = models.CharField("제목", max_length=200)
    author = models.CharField("저자", max_length=100, blank=True)
    status = models.CharField("읽는 상태", max_length=10, choices=Status.choices, default=Status.WANT)
    rating = models.PositiveSmallIntegerField("별점", null=True, blank=True)
    finished_on = models.DateField("다 읽은 날", null=True, blank=True)
    cover = models.ImageField("표지", upload_to="covers/", blank=True)
    summary = models.TextField("메모 요약", blank=True)
    summary_by_ai = models.BooleanField("AI가 만든 요약", default=False)
    tags = models.CharField("태그", max_length=100, blank=True, help_text="쉼표로 나눈다")
    tags_by_ai = models.BooleanField("AI가 붙인 태그", default=False)
    created_at = models.DateTimeField("등록한 때", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def tag_list(self):
        return [t.strip() for t in self.tags.split(",") if t.strip()]

    @property
    def stars(self):
        """별점을 별 모양으로 보여 준다. 예: 4점이면 ★★★★"""
        return "★" * (self.rating or 0)



class Note(models.Model):
    """책 한 권에 여러 개 다는 독서 메모."""

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="notes", verbose_name="책")
    body = models.TextField("메모")
    created_at = models.DateTimeField("쓴 때", auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.book.title}의 메모"


class AICall(models.Model):
    """AI 기능을 부를 때마다 남기는 기록. 하루 사용 횟수와 중복 실행을 막는 데도 쓴다."""

    class Status(models.TextChoices):
        RUNNING = "running", "실행 중"
        OK = "ok", "성공"
        ERROR = "error", "실패"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="사용자")
    feature = models.CharField("기능", max_length=20)
    status = models.CharField("결과", max_length=10, choices=Status.choices, default=Status.RUNNING)
    seconds = models.FloatField("걸린 시간(초)", null=True, blank=True)
    error = models.CharField("오류", max_length=200, blank=True)
    created_at = models.DateTimeField("부른 때", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "AI 호출 기록"
        verbose_name_plural = "AI 호출 기록"

    def __str__(self):
        return f"{timezone.localtime(self.created_at):%Y-%m-%d %H:%M} {self.feature} {self.get_status_display()}"
