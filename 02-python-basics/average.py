# practice-files/broken_average.py를 고친 판
scores = ["80", "92", "75"]


def average(values):
    total = 0
    for value in values:
        total = total + int(value)
    return total / len(values)


print("평균 점수:", average(scores))
print("최고 점수:", max(int(s) for s in scores))
