import json

from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .ai import AIError, ask_codex
from .models import Quiz, StudyNote
from .prompts import QUIZ, build_prompt

QUIZ_SCHEMA = settings.BASE_DIR / "study" / "schemas" / "quiz.json"


class NoteForm(forms.ModelForm):
    class Meta:
        model = StudyNote
        fields = ["subject", "title", "body"]
        widgets = {"body": forms.Textarea(attrs={"rows": 6})}


@login_required
def note_list(request):
    form = NoteForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        note = form.save(commit=False)
        note.owner = request.user
        note.save()
        return redirect("note_detail", pk=note.pk)
    notes = StudyNote.objects.filter(owner=request.user)
    wrong = Quiz.objects.filter(note__owner=request.user, wrong_count__gt=0).count()
    return render(request, "study/note_list.html", {"form": form, "notes": notes, "wrong": wrong})


@login_required
def note_detail(request, pk):
    note = get_object_or_404(StudyNote, pk=pk, owner=request.user)
    return render(request, "study/note_detail.html", {"note": note})


def valid_question(q):
    return (
        isinstance(q.get("question"), str)
        and isinstance(q.get("choices"), list) and len(q["choices"]) == 4
        and isinstance(q.get("answer"), int) and 0 <= q["answer"] <= 3
    )


@login_required
def make_quiz(request, pk):
    note = get_object_or_404(StudyNote, pk=pk, owner=request.user)
    if request.method != "POST":
        return redirect("note_detail", pk=note.pk)
    try:
        answer = ask_codex(build_prompt(QUIZ, f"과목: {note.subject}\n제목: {note.title}\n{note.body}"), QUIZ_SCHEMA)
        questions = [q for q in json.loads(answer)["questions"] if valid_question(q)]
    except AIError as error:
        messages.error(request, str(error))
        return redirect("note_detail", pk=note.pk)
    except (ValueError, KeyError, TypeError):
        messages.error(request, "AI의 답을 읽지 못했습니다. 다시 시도하세요.")
        return redirect("note_detail", pk=note.pk)
    note.quizzes.all().delete()
    for q in questions:
        Quiz.objects.create(note=note, question=q["question"], choices=q["choices"],
                            answer=q["answer"], explanation=q.get("explanation", ""))
    messages.success(request, f"문제 {len(questions)}개를 만들었습니다. 정답과 해설이 노트와 맞는지 확인하세요.")
    return redirect("solve", pk=note.pk)


def grade(request, quizzes):
    """제출한 답을 채점하고 틀린 문제의 틀린 횟수를 올린다."""
    results = []
    for quiz in quizzes:
        picked = request.POST.get(f"q{quiz.pk}")
        correct = picked is not None and int(picked) == quiz.answer
        if not correct:
            quiz.wrong_count += 1
        elif quiz.wrong_count:
            quiz.wrong_count -= 1
        quiz.save(update_fields=["wrong_count"])
        results.append({"quiz": quiz, "correct": correct})
    return results


@login_required
def solve(request, pk):
    note = get_object_or_404(StudyNote, pk=pk, owner=request.user)
    quizzes = list(note.quizzes.all())
    results = grade(request, quizzes) if request.method == "POST" else None
    return render(request, "study/solve.html", {"title": note.title, "quizzes": quizzes, "results": results})


@login_required
def review(request):
    """틀린 적이 있는 문제만 다시 푼다."""
    quizzes = list(Quiz.objects.filter(note__owner=request.user, wrong_count__gt=0))
    results = grade(request, quizzes) if request.method == "POST" else None
    return render(request, "study/solve.html", {"title": "틀린 문제 다시 풀기", "quizzes": quizzes, "results": results})
