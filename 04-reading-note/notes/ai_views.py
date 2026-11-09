"""AI 기능 화면: 메모 요약, 태그 분류, 다음 책 추천, AI 결과 고치기."""
import json
import time
from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from . import prompts
from .ai import AIError, ask_codex
from .models import AICall, Book
from .views import my_book

TAGS_SCHEMA = settings.BASE_DIR / "notes" / "schemas" / "tags.json"


def run_ai(request, feature, prompt, schema_file=None):
    """기록을 남기며 Codex를 부른다. 막히면 None을 돌려주고 안내 문구를 띄운다."""
    today = timezone.localdate()
    if AICall.objects.filter(user=request.user, created_at__date=today).count() >= settings.AI_DAILY_LIMIT:
        messages.error(request, f"오늘은 AI 기능을 {settings.AI_DAILY_LIMIT}번 모두 썼습니다. 내일 다시 쓸 수 있습니다.")
        return None
    recent = timezone.now() - timedelta(minutes=3)
    if AICall.objects.filter(user=request.user, status=AICall.Status.RUNNING, created_at__gte=recent).exists():
        messages.error(request, "AI가 아직 앞의 요청을 처리하고 있습니다. 끝난 뒤 다시 누르세요.")
        return None

    call = AICall.objects.create(user=request.user, feature=feature)
    started = time.monotonic()
    try:
        answer = ask_codex(prompt, schema_file)
    except AIError as error:
        call.status, call.error = AICall.Status.ERROR, str(error)[:200]
        messages.error(request, str(error))
        answer = None
    else:
        call.status = AICall.Status.OK
    call.seconds = round(time.monotonic() - started, 1)
    call.save()
    return answer


@login_required
@require_POST
def summarize(request, pk):
    book = my_book(request, pk)
    memo = "\n\n".join(note.body for note in book.notes.all())
    if not memo:
        messages.error(request, "요약할 메모가 없습니다. 메모를 먼저 남기세요.")
        return redirect("book_detail", pk=book.pk)
    answer = run_ai(request, "요약", prompts.build_prompt(prompts.SUMMARY, memo))
    if answer:
        book.summary, book.summary_by_ai = answer, True
        book.save(update_fields=["summary", "summary_by_ai"])
        messages.success(request, "메모를 요약했습니다. 메모와 맞는지 확인하세요.")
    return redirect("book_detail", pk=book.pk)


@login_required
@require_POST
def tag(request, pk):
    book = my_book(request, pk)
    data = f"제목: {book.title}\n저자: {book.author}\n메모:\n" + "\n".join(n.body for n in book.notes.all())
    data += "\n\n태그 목록: " + ", ".join(prompts.TAG_CHOICES)
    answer = run_ai(request, "태그", prompts.build_prompt(prompts.TAGS, data), TAGS_SCHEMA)
    if answer:
        try:
            picked = json.loads(answer)["tags"]
        except (ValueError, KeyError, TypeError):
            messages.error(request, "AI의 답을 읽지 못했습니다. 다시 시도하세요.")
            return redirect("book_detail", pk=book.pk)
        tags = [t for t in picked if t in prompts.TAG_CHOICES][:3]  # 목록에 없는 태그는 버린다
        book.tags, book.tags_by_ai = ", ".join(tags), True
        book.save(update_fields=["tags", "tags_by_ai"])
        messages.success(request, "태그를 붙였습니다. 어울리지 않으면 고치세요.")
    return redirect("book_detail", pk=book.pk)


@login_required
@require_POST
def edit_ai(request, pk):
    """AI가 만든 요약과 태그를 사람이 고쳐 확정한다."""
    book = my_book(request, pk)
    book.summary = request.POST.get("summary", "").strip()
    tags = [t.strip() for t in request.POST.get("tags", "").split(",") if t.strip()]
    book.tags = ", ".join(tags)
    book.summary_by_ai = book.tags_by_ai = False
    book.save(update_fields=["summary", "tags", "summary_by_ai", "tags_by_ai"])
    messages.success(request, "요약과 태그를 확인해 저장했습니다.")
    return redirect("book_detail", pk=book.pk)


@login_required
def recommend(request):
    favorites = Book.objects.filter(owner=request.user, rating__gte=4).order_by("-rating")[:10]
    answer = None
    if request.method == "POST":
        if not favorites:
            messages.error(request, "별점 4점 이상인 책이 있어야 추천받을 수 있습니다.")
        else:
            lines = [f"- {b.title} / {b.author} (별점 {b.rating}) {b.summary[:120]}" for b in favorites]
            answer = run_ai(request, "추천", prompts.build_prompt(prompts.RECOMMEND, "\n".join(lines)))
    items = []
    for line in (answer or "").splitlines():
        line = line.strip().lstrip("-").strip()
        if line:
            # '제목 / 저자: 이유'에서 제목과 저자만 떼어 검색어로 쓴다.
            items.append({"text": line, "query": " ".join(line.split(":")[0].replace("/", " ").split())})
    return render(request, "notes/recommend.html", {"favorites": favorites, "items": items})
