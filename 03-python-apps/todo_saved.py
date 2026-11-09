from pathlib import Path

# 이 파일과 같은 폴더의 todo.txt에 저장한다.
TODO_FILE = Path(__file__).parent / "todo.txt"


def load():
    """파일에서 할 일을 읽어 온다. 파일이 없으면 빈 목록."""
    if not TODO_FILE.exists():
        return []
    text = TODO_FILE.read_text(encoding="utf-8")
    return [line for line in text.splitlines() if line.strip()]


def save(todos):
    """할 일을 한 줄에 하나씩 파일에 저장한다."""
    TODO_FILE.write_text("\n".join(todos) + "\n", encoding="utf-8")


def show(todos):
    print()
    print("[할 일 목록]")
    if not todos:
        print("  (비어 있음)")
    for number, item in enumerate(todos, start=1):
        print(f"  {number}. {item}")


def main():
    todos = load()
    while True:
        show(todos)
        print("1) 더하기  2) 지우기  3) 끝내기")
        menu = input("번호를 고르세요: ").strip()
        if menu == "1":
            item = input("할 일: ").strip()
            if item:
                todos.append(item)
                save(todos)
        elif menu == "2":
            number = input("지울 번호: ").strip()
            if number.isdigit() and 1 <= int(number) <= len(todos):
                removed = todos.pop(int(number) - 1)
                save(todos)
                print(f"'{removed}'을(를) 지웠습니다.")
            else:
                print("목록에 있는 번호를 입력해 주세요.")
        elif menu == "3":
            print("저장하고 끝냅니다.")
            break
        else:
            print("1, 2, 3 가운데 하나를 고르세요.")


main()
