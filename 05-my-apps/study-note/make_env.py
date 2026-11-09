""".env가 없으면 .env.example을 바탕으로 무작위 비밀 키를 넣어 만든다.

실행: uv run python make_env.py
"""
from pathlib import Path

from django.core.management.utils import get_random_secret_key

here = Path(__file__).parent
env_file = here / ".env"
if env_file.exists():
    print(".env가 이미 있습니다. 그대로 둡니다.")
else:
    text = (here / ".env.example").read_text(encoding="utf-8")
    text = text.replace("여기에-긴-무작위-문자열", get_random_secret_key())
    env_file.write_text(text, encoding="utf-8")
    print(".env를 만들었습니다. 이 파일은 남에게 보내거나 Git에 올리지 마세요.")
