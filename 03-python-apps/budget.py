import csv
from pathlib import Path

HERE = Path(__file__).parent
SOURCE = HERE.parent / "practice-files" / "budget.csv"
RESULT = HERE / "budget_summary.csv"

totals = {}
# utf-8-sig: 엑셀이 저장한 CSV 맨 앞의 표시(BOM)를 함께 처리한다.
with open(SOURCE, encoding="utf-8-sig", newline="") as f:
    for row in csv.DictReader(f):
        amount = int(row["금액"].replace(",", ""))
        totals[row["항목"]] = totals.get(row["항목"], 0) + amount

ranking = sorted(totals.items(), key=lambda pair: pair[1], reverse=True)

print("[항목별 합계]")
for category, amount in ranking:
    print(f"  {category}: {amount:,}원")
print(f"전체 합계: {sum(totals.values()):,}원")
print(f"가장 많이 쓴 항목: {ranking[0][0]}")

# 엑셀에서 한글이 깨지지 않게 utf-8-sig로 저장한다.
with open(RESULT, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["항목", "합계"])
    writer.writerows(ranking)
print(f"요약을 {RESULT.name}에 저장했습니다.")
