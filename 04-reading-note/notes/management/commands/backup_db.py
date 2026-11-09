"""db.sqlite3를 backups 폴더에 날짜를 붙여 복사한다.

    uv run python manage.py backup_db
되살릴 때는 서버를 끄고, 백업 파일을 db.sqlite3라는 이름으로 덮어 복사한다.
"""
import sqlite3
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "데이터베이스를 backups/db-날짜-시각.sqlite3로 백업한다."

    def handle(self, *args, **options):
        source = settings.DATABASES["default"]["NAME"]
        folder = settings.BASE_DIR / "backups"
        folder.mkdir(exist_ok=True)
        target = folder / f"db-{datetime.now():%Y%m%d-%H%M%S}.sqlite3"
        # SQLite의 백업 기능으로 복사하면 쓰는 중이어도 깨지지 않은 사본이 생긴다.
        with sqlite3.connect(source) as src, sqlite3.connect(target) as dst:
            src.backup(dst)
        self.stdout.write(self.style.SUCCESS(f"백업했습니다: {target.relative_to(settings.BASE_DIR)}"))
