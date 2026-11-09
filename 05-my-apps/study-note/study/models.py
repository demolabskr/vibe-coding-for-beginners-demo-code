from django.conf import settings
from django.db import models


class StudyNote(models.Model):
    """공부한 내용을 적은 노트."""

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="주인")
    subject = models.CharField("과목", max_length=50)
    title = models.CharField("제목", max_length=200)
    body = models.TextField("공부한 내용")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.subject}] {self.title}"


class Quiz(models.Model):
    """노트로 만든 사지선다 문제 하나."""

    note = models.ForeignKey(StudyNote, on_delete=models.CASCADE, related_name="quizzes")
    question = models.TextField("문제")
    choices = models.JSONField("보기")  # 보기 네 개의 목록
    answer = models.PositiveSmallIntegerField("정답 번호")  # 0부터 3까지
    explanation = models.TextField("해설")
    wrong_count = models.PositiveIntegerField("틀린 횟수", default=0)

    def __str__(self):
        return self.question[:30]
