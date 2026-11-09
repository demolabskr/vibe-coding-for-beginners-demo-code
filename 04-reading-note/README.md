# 나의 독서 노트 (04-reading-note)

책을 등록하고 메모를 남기며, 내 컴퓨터의 Codex로 메모 요약, 태그 분류, 다음 책 추천을 받는 Django 웹앱이다.
내 컴퓨터에서 나 혼자 쓰는 웹앱이다. 인터넷이나 같은 와이파이의 다른 기기에 열지 않는다.

## 처음 한 번 준비

모든 명령은 PowerShell에서 실행한다.

1. 실습 프로젝트 루트(`vibe-coding`)에서 파이썬 환경을 맞춘다.
   ```powershell
   uv sync
   ```
2. `04-reading-note` 폴더로 옮겨 비밀 키 파일 `.env`를 만든다.
   ```powershell
   cd 04-reading-note
   uv run python make_env.py
   ```
3. 데이터베이스 표를 만들고 관리자 계정을 만든다(비밀번호는 직접 입력한다).
   ```powershell
   uv run python manage.py migrate
   uv run python manage.py createsuperuser
   ```
4. AI 기능을 쓰려면 Codex 명령이 로그인돼 있어야 한다.
   ```powershell
   codex login status
   ```
   `Logged in using ChatGPT`가 나오면 된다. 아니면 `codex login`으로 데스크톱 앱과 같은 ChatGPT 계정으로 로그인한다.

## 켜고 끄기

```powershell
.\start.ps1
```

`.env` 확인, `migrate`, 서버 켜기를 차례로 하고 3초 뒤 브라우저로 `http://127.0.0.1:8000/`을 연다. 끌 때는 그 창에서 `Ctrl+C`를 누른다.
스크립트 실행이 막히면(실행 정책 오류) 이렇게 실행한다.

```powershell
powershell -ExecutionPolicy Bypass -File .\start.ps1
```

## 자주 쓰는 명령

| 하는 일 | 명령 |
|---|---|
| 테스트 | `uv run python manage.py test` |
| 데이터베이스 백업 | `uv run python manage.py backup_db` (backups 폴더에 날짜를 붙여 저장) |
| 파이썬 앱의 책 옮기기 | `uv run python manage.py import_books` (미리보기), 끝에 `--apply`를 붙이면 옮긴다 |
| 실습용 가짜 책 50권 | `uv run python manage.py make_sample_books 사용자이름` |
| Codex 호출 시험 | `uv run python ask.py "물어볼 말"` |

## 백업에서 되살리기

1. 서버를 끈다(`Ctrl+C`).
2. `backups` 폴더의 백업 파일을 `db.sqlite3`라는 이름으로 덮어 복사한다.
3. 서버를 다시 켠다.

## 자주 나는 오류

| 보이는 문구 | 할 일 |
|---|---|
| `.env에 DJANGO_SECRET_KEY가 없습니다` | `uv run python make_env.py` |
| `no such table` | `uv run python manage.py migrate` |
| `That port is already in use` | 이미 켜 둔 서버 창을 찾아 끄거나 `runserver 127.0.0.1:8001`로 다른 포트를 쓴다 |
| `codex 명령을 찾을 수 없습니다` | Codex 명령을 설치하고 새 PowerShell 창을 연다 |
| `Codex 로그인이 풀렸습니다` | `codex login` |
| `오늘은 AI 기능을 20번 모두 썼습니다` | 다음 날 다시 쓰거나 `config/settings.py`의 `AI_DAILY_LIMIT`를 바꾼다 |
