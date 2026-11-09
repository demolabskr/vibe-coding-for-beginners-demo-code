def ask_number(message):
    """숫자를 받을 때까지 다시 묻는다."""
    while True:
        text = input(message)
        try:
            return float(text)
        except ValueError:
            print("숫자로 입력해 주세요. 예: 12 또는 3.5")


a = ask_number("첫 번째 숫자: ")
b = ask_number("두 번째 숫자: ")

print("더하기:", a + b)
print("빼기:", a - b)
print("곱하기:", a * b)
if b == 0:
    print("나누기: 0으로는 나눌 수 없습니다.")
else:
    print("나누기:", a / b)
