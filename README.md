# 비개발 초보자를 위한 바이브 코딩 입문 - Codex 활용편, 예시 코드

책 「비개발 초보자를 위한 바이브 코딩 입문 - Codex 활용편」을 따라 만든 실습 프로젝트입니다.
지은이가 Windows에서 ChatGPT 데스크톱 앱의 Codex에게 책의 요청문을 보내 만든 결과를 정리했습니다.
Codex의 결과는 같은 요청에도 매번 조금씩 다르므로, 여러분의 코드가 이 저장소와 똑같지 않아도 됩니다.
막히거나 결과가 이상할 때 같은 부의 코드와 비교해 보세요.

## 폴더 구조

```text
vibe-coding/              실습 프로젝트(이 저장소). Git 저장소와 uv 환경(pyproject.toml, uv.lock)이 루트에 하나
├─ AGENTS.md              Codex가 읽는 실습 규칙
├─ docs/                  idea.md(독서 노트 기획 메모), features.md(기능 목록), data-design.md(데이터 설계표),
│                         review.md(코드 검토 결과), my-idea.md·my-app.md(지은이의 아이디어 메모와 설계: 업무 일지)
├─ 01-warmup/             1-2부 HTML 연습
├─ 02-python-basics/      3부 파이썬 첫 프로그램
├─ 03-python-apps/        4부 파일·CSV·SQLite를 다루는 프로그램, 독서 기록 프로그램(book_cli)
├─ 04-reading-note/       5-9부 Django 웹앱 「나의 독서 노트」
├─ 05-my-apps/            10부 예시 웹앱: work-log(업무 일지), study-note(공부 노트)
├─ ai_box/                웹앱이 Codex를 부를 때 쓰는 빈 폴더(비워 둔다)
└─ practice-files/        실습 자료(가상 가계부 CSV, 오류 실습 파일, 이름 정리용 빈 사진 파일)
```

## 부별 태그

부가 끝날 때마다 태그를 남겼습니다. GitHub에서 브랜치·태그 선택 상자로 태그를 고르면 그 부가 끝났을 때의 코드를 볼 수 있습니다.

| 태그 | 끝난 부 | 주요 결과 |
|---|---|---|
| `part-01` | 1부 바이브 코딩과 Codex 시작하기 | 01-warmup/today.html |
| `part-02` | 2부 실습 프로젝트와 작업 환경 준비 | 단계별 폴더, pyproject.toml, AGENTS.md, pledge.html, docs/idea.md |
| `part-03` | 3부 파이썬 첫걸음 | 02-python-basics의 프로그램 |
| `part-04` | 4부 파이썬 일반 앱 | 03-python-apps, docs/features.md |
| `part-05` | 5부 웹의 원리와 Django 시작 | 04-reading-note의 첫 페이지와 공통 틀 |
| `part-06` | 6부 데이터베이스와 Django 모델 | 모델, 관리자 화면, 목록과 상세, 데이터 옮기기와 백업 |
| `part-07` | 7부 사용자가 쓰는 웹앱 기능 | 입력 양식, 검색과 정렬, 통계, 표지, 로그인과 사용자별 데이터 |
| `part-08` | 8부 Codex 불러 AI 기능 붙이기 | 메모 요약, 태그 분류, 다음 책 추천, AI 사용 기록 |
| `part-09` | 9부 점검하고 다듬기 | 테스트, .env, README, start.ps1 |
| `part-10` | 10부 나만의 웹앱으로 넓히기 | 05-my-apps, 다듬은 AGENTS.md |

## Windows에서 준비하기

책은 Windows만 설명합니다. 명령은 모두 PowerShell에서 실행합니다.

1. ChatGPT 데스크톱 앱(유료 계정)을 설치하고 로그인합니다(Microsoft Store).
2. Git, Python, uv를 설치합니다. 책에서는 Codex에게 winget으로 설치를 맡깁니다.
3. AI 기능(8부부터)을 쓰려면 Codex 명령(CLI)을 공식 안내(https://learn.chatgpt.com/docs/cli)에 따라 설치하고, 데스크톱 앱과 같은 ChatGPT 계정으로 로그인합니다. `codex login status`로 확인합니다.

## 내려받아 실행하기

```powershell
git clone https://github.com/demolabskr/vibe-coding-for-beginners-demo-code.git vibe-coding
cd vibe-coding
uv sync
```

Git이 없으면 GitHub의 Code 단추에서 ZIP으로 내려받아 압축을 풀어도 됩니다.

| 폴더 | 실행 |
|---|---|
| 02-python-basics, 03-python-apps | `uv run python 02-python-basics\hello.py`처럼 루트에서 실행 |
| 04-reading-note | `04-reading-note\README.md`를 본다. 처음에는 `make_env.py`, `migrate`, `createsuperuser`를 한 번씩 하고, 그다음부터는 `.\start.ps1` |
| 05-my-apps\work-log, study-note | 각 폴더에서 `uv run python make_env.py`, `uv run python manage.py migrate`, `uv run python manage.py createsuperuser`, `uv run python manage.py runserver` |

## 알아 둘 것

- 웹앱의 AI 기능은 API 키 없이 내 컴퓨터의 Codex를 `codex exec`로 부릅니다. 요금제의 Codex 사용량을 코딩 작업과 함께 쓰므로 하루 사용 횟수를 제한해 두었습니다.
- 이 방식은 내 컴퓨터에서 나 혼자 쓰는 웹앱에만 씁니다. 웹앱을 인터넷이나 같은 와이파이의 다른 기기에 열지 마세요.
- 실습 자료와 예시 기록은 모두 가상입니다.

## 라이선스

MIT. `LICENSE`를 보세요.
