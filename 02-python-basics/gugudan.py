import random

QUESTION_COUNT = 5
wrong = []
score = 0

for number in range(1, QUESTION_COUNT + 1):
    a = random.randint(2, 9)
    b = random.randint(1, 9)
    answer = input(f"{number}번. {a} x {b} = ")
    if answer.strip() == str(a * b):
        print("정답!")
        score += 1
    else:
        print(f"아쉬워요. 정답은 {a * b}입니다.")
        wrong.append((a, b))

print(f"{QUESTION_COUNT}문제 가운데 {score}문제를 맞혔습니다.")

while wrong:
    print("틀린 문제를 다시 풀어 봅시다.")
    again = []
    for a, b in wrong:
        answer = input(f"{a} x {b} = ")
        if answer.strip() == str(a * b):
            print("이번에는 정답!")
        else:
            print(f"정답은 {a * b}입니다.")
            again.append((a, b))
    wrong = again

print("모든 문제를 맞혔습니다. 수고했어요!")
