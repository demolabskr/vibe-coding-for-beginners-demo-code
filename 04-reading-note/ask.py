"""웹앱에 붙이기 전에 Codex 호출 함수를 시험하는 짧은 스크립트.

실행: uv run python 04-reading-note/ask.py "물어볼 말"
"""
import sys

from notes.ai import AIError, ask_codex

question = " ".join(sys.argv[1:]) or "책 「아몬드」(손원평)를 한 문장으로 소개해 줘."
try:
    print(ask_codex(question + "\n파일을 열거나 명령을 실행하지 말고 답만 써."))
except AIError as error:
    print("오류:", error)
