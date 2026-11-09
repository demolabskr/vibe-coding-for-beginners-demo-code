todos = []

while True:
    print()
    print("[할 일 목록]")
    if not todos:
        print("  (비어 있음)")
    for number, item in enumerate(todos, start=1):
        print(f"  {number}. {item}")
    print("1) 더하기  2) 지우기  3) 끝내기")
    menu = input("번호를 고르세요: ").strip()

    if menu == "1":
        item = input("할 일: ").strip()
        if item:
            todos.append(item)
    elif menu == "2":
        number = input("지울 번호: ").strip()
        if number.isdigit() and 1 <= int(number) <= len(todos):
            removed = todos.pop(int(number) - 1)
            print(f"'{removed}'을(를) 지웠습니다.")
        else:
            print("목록에 있는 번호를 입력해 주세요.")
    elif menu == "3":
        print("프로그램을 끝냅니다.")
        break
    else:
        print("1, 2, 3 가운데 하나를 고르세요.")
