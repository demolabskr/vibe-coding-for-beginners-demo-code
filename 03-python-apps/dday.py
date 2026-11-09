from datetime import date

from dateutil import parser
from dateutil.relativedelta import relativedelta

text = input("기념일이나 마감일을 입력하세요 (예: 2026-12-25): ")
target = parser.parse(text).date()
today = date.today()
days = (target - today).days

if days > 0:
    print(f"D-{days}: 앞으로 {days}일 남았습니다.")
elif days == 0:
    print("D-Day: 바로 오늘입니다!")
else:
    print(f"D+{-days}: {-days}일 지났습니다.")

gap = relativedelta(target, today)
print(f"달력으로는 {abs(gap.years)}년 {abs(gap.months)}개월 {abs(gap.days)}일 차이입니다.")
