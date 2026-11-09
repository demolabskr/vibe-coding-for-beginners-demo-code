from django.conf import settings
from django.db import models
from django.utils import timezone


class Entry(models.Model):
    """하루 업무 기록 한 줄."""

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="주인")
    day = models.DateField("날짜", default=timezone.localdate)
    body = models.TextField("한 일")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-day", "-created_at"]

    def __str__(self):
        return f"{self.day} {self.body[:20]}"


class WeeklyReport(models.Model):
    """한 주의 기록으로 만든 주간 보고 초안."""

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="주인")
    week_start = models.DateField("주 시작일(월요일)")
    body = models.TextField("보고 내용")
    by_ai = models.BooleanField("AI가 만든 초안", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-week_start"]
        unique_together = [("owner", "week_start")]
