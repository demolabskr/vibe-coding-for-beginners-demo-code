"""내 컴퓨터의 Codex를 불러 답을 받는다(codex exec). 04-reading-note/notes/ai.py를 가져와 AI_BOX 경로만 고쳤다.

데스크톱 앱과 같은 ChatGPT 계정으로 로그인한 codex 명령을 쓴다. API 키는 필요 없고,
요금제의 Codex 사용량을 함께 쓴다. 내 컴퓨터에서 나 혼자 쓰는 웹앱에만 쓴다.
"""
import shutil
import subprocess
from pathlib import Path

# 실습 프로젝트 루트의 빈 폴더. Codex는 이 폴더를 작업 위치로 삼는다.
AI_BOX = Path(__file__).resolve().parents[3] / "ai_box"  # 05-my-apps 아래로 한 단계 더 깊어 3으로 바꿨다
TIMEOUT_SECONDS = 120


class AIError(Exception):
    """사용자에게 그대로 보여 줄 수 있는 문장을 담은 오류."""


def ask_codex(prompt, schema_file=None, timeout=TIMEOUT_SECONDS):
    """요청문(prompt)을 Codex에 보내고 마지막 답 글자를 돌려준다."""
    codex = shutil.which("codex")  # Windows에서는 codex.cmd 같은 실제 파일을 찾아 준다
    if codex is None:
        raise AIError("codex 명령을 찾을 수 없습니다. Codex 명령을 설치했는지 확인하세요.")

    command = [
        codex, "exec",
        "--sandbox", "read-only",       # 파일을 바꾸거나 명령으로 무언가를 고칠 수 없게 한다
        "--cd", str(AI_BOX),            # 빈 폴더를 작업 위치로 삼는다
        "--skip-git-repo-check",        # Git 저장소 밖으로 옮겨도 동작하게 한다
        "--ephemeral",                  # 대화 기록 파일을 남기지 않는다
        "--ignore-user-config",         # 내 Codex 개인 설정(연결한 도구 등)을 쓰지 않는다
        "-c", "project_doc_max_bytes=0",  # AGENTS.md 같은 규칙 파일을 읽지 않는다
        "--color", "never",
    ]
    if schema_file:
        command += ["--output-schema", str(schema_file)]
    command.append("-")  # 요청문은 표준 입력으로 넘긴다(긴 글과 한글도 안전하다)

    try:
        result = subprocess.run(
            command, input=prompt, capture_output=True, text=True, encoding="utf-8", timeout=timeout
        )
    except subprocess.TimeoutExpired:
        raise AIError(f"{timeout}초 안에 답이 오지 않았습니다. 잠시 뒤 다시 시도하세요.")

    if result.returncode != 0:
        raise AIError(explain(result.stderr))
    answer = result.stdout.strip()
    if not answer:
        raise AIError("Codex가 빈 답을 돌려줬습니다. 다시 시도하세요.")
    return answer


def explain(stderr):
    """codex의 오류 출력을 사용자가 알아듣는 문장으로 바꾼다."""
    text = stderr.lower()
    if "login" in text or "logged in" in text or "unauthorized" in text or "401" in text:
        return "Codex 로그인이 풀렸습니다. 터미널에서 codex login으로 다시 로그인하세요."
    if "usage limit" in text or "rate limit" in text or "429" in text:
        return "요금제의 Codex 사용량 한도에 닿았습니다. 한도가 풀린 뒤 다시 시도하세요."
    if "network" in text or "connect" in text or "dns" in text:
        return "인터넷 연결을 확인하세요. Codex가 서버에 닿지 못했습니다."
    return "Codex 실행에 실패했습니다. 터미널에서 codex login status로 상태를 확인하세요."
