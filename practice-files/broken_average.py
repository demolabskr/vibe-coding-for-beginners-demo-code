# 오류 실습 파일: 일부러 오류를 넣어 두었다. 실행하면 빨간 오류가 난다.
scores = ["80", "92", "75"]

def average(values):
    total = 0
    for value in values:
        total = total + value
    return total / len(values)

print("평균 점수:", average(scores))
print("최고 점수:", max(score))
