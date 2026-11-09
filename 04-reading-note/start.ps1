# 나의 독서 노트를 켠다. 끄려면 이 창에서 Ctrl+C를 누른다.
# 실행: 04-reading-note 폴더에서 .\start.ps1
Set-Location $PSScriptRoot

Write-Host "1/3 .env 확인"
uv run python make_env.py

Write-Host "2/3 데이터베이스 표 맞추기(migrate)"
uv run python manage.py migrate

Write-Host "3/3 서버 켜기: http://127.0.0.1:8000/"
# 서버가 켜질 시간을 3초 준 뒤 브라우저를 연다.
Start-Job { Start-Sleep -Seconds 3; Start-Process "http://127.0.0.1:8000/" } | Out-Null
uv run python manage.py runserver 127.0.0.1:8000
