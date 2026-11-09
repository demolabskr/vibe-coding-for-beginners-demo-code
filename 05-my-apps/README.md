# 05-my-apps

10부에서 독서 노트의 순서(기획 메모 → 기능 목록 → 데이터 설계 → 화면 → AI 기능)를 다른 아이디어에 옮겨 만든 예시 웹앱이다.
두 앱 모두 `04-reading-note/notes/ai.py`의 Codex 호출 함수를 가져와 `AI_BOX` 경로만 고쳐 쓴다.

| 폴더 | 웹앱 | AI 기능 |
|---|---|---|
| `work-log` | 업무 일지: 날짜별로 한 일을 적는다 | 한 주의 기록으로 주간 보고 초안 만들기 |
| `study-note` | 공부 노트: 과목별로 공부한 내용을 적는다 | 노트로 사지선다 복습 퀴즈 만들기(형식 있는 답), 틀린 문제 다시 풀기 |

각 폴더에서 처음 한 번:

```powershell
uv run python make_env.py
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

회사 업무 기록을 AI에 넣기 전에는 회사의 AI 사용 규정을 먼저 확인한다.
