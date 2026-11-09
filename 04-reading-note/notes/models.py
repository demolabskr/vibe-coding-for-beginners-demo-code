from django.db import models


class Book(models.Model):
    """책 한 권. docs/data-design.md의 책 표와 같다."""

    class Status(models.TextChoices):
        WANT = "want", "읽고 싶음"
        READING = "reading", "읽는 중"
        DONE = "done", "다 읽음"

    title = models.CharField("제목", max_length=200)
    author = models.CharField("저자", max_length=100, blank=True)
    status = models.CharField("읽는 상태", max_length=10, choices=Status.choices, default=Status.WANT)
    rating = models.PositiveSmallIntegerField("별점", null=True, blank=True)
    finished_on = models.DateField("다 읽은 날", null=True, blank=True)
    created_at = models.DateTimeField("등록한 때", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title



class Note(models.Model):
    """책 한 권에 여러 개 다는 독서 메모."""

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="notes", verbose_name="책")
    body = models.TextField("메모")
    created_at = models.DateTimeField("쓴 때", auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.book.title}의 메모"
