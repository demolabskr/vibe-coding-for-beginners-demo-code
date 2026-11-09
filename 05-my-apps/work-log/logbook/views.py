from datetime import timedelta

from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from .ai import AIError, ask_codex
from .models import Entry, WeeklyReport
from .prompts import WEEKLY_REPORT, build_prompt


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["day", "body"]
        widgets = {"day": forms.DateInput(attrs={"type": "date"}), "body": forms.Textarea(attrs={"rows": 2})}


def monday_of(day):
    return day - timedelta(days=day.weekday())


@login_required
def entry_list(request):
    form = EntryForm(request.POST or None, initial={"day": timezone.localdate()})
    if request.method == "POST" and form.is_valid():
        entry = form.save(commit=False)
        entry.owner = request.user
        entry.save()
        messages.success(request, "기록했습니다.")
        return redirect("entry_list")
    week_start = monday_of(timezone.localdate())
    entries = Entry.objects.filter(owner=request.user, day__gte=week_start - timedelta(days=7))
    return render(request, "logbook/entry_list.html", {"form": form, "entries": entries, "week_start": week_start})


@login_required
def weekly_report(request):
    week_start = monday_of(timezone.localdate())
    if request.GET.get("week") == "last":
        week_start -= timedelta(days=7)
    week_end = week_start + timedelta(days=6)
    entries = Entry.objects.filter(owner=request.user, day__range=(week_start, week_end)).order_by("day")
    report = WeeklyReport.objects.filter(owner=request.user, week_start=week_start).first()

    if request.method == "POST":
        if not entries:
            messages.error(request, "이 주에 적은 기록이 없습니다.")
        else:
            data = "\n".join(f"{e.day:%m/%d(%a)} {e.body}" for e in entries)
            try:
                body = ask_codex(build_prompt(WEEKLY_REPORT, data))
            except AIError as error:
                messages.error(request, str(error))
            else:
                report, _ = WeeklyReport.objects.update_or_create(
                    owner=request.user, week_start=week_start, defaults={"body": body, "by_ai": True}
                )
                messages.success(request, "주간 보고 초안을 만들었습니다. 기록과 맞는지 확인하세요.")
        return redirect(request.get_full_path())
    return render(request, "logbook/weekly_report.html", {
        "week_start": week_start, "week_end": week_end, "entries": entries, "report": report,
    })
