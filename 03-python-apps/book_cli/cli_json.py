"""독서 기록 프로그램 JSON판: 책을 books.json에 저장한다."""
import json
from pathlib import Path

BOOKS_FILE = Path(__file__).parent / "books.json"
STATUSES = {"1": "읽고 싶음", "2": "읽는 중", "3": "다 읽음"}


def load():
    if not BOOKS_FILE.exists():
        return []
    return json.loads(BOOKS_FILE.read_text(encoding="utf-8"))


def save(books):
    BOOKS_FILE.write_text(json.dumps(books, ensure_ascii=False, indent=2), encoding="utf-8")


def show(books):
    if not books:
        print("  (책이 없습니다)")
    for number, book in enumerate(books, start=1):
        print(f"  {number}. {book['title']} / {book['author']} [{book['status']}]")


def add(books):
    title = input("제목: ").strip()
    author = input("저자: ").strip()
    if not title:
        print("제목은 꼭 입력해 주세요.")
        return
    books.append({"title": title, "author": author, "status": "읽고 싶음"})
    save(books)
    print(f"'{title}'을(를) 등록했습니다.")


def search(books):
    word = input("찾을 말(제목이나 저자): ").strip()
    found = [b for b in books if word in b["title"] or word in b["author"]]
    show(found)


def change_status(books):
    show(books)
    number = input("상태를 바꿀 책 번호: ").strip()
    if not (number.isdigit() and 1 <= int(number) <= len(books)):
        print("목록에 있는 번호를 입력해 주세요.")
        return
    choice = input("1) 읽고 싶음  2) 읽는 중  3) 다 읽음: ").strip()
    if choice in STATUSES:
        books[int(number) - 1]["status"] = STATUSES[choice]
        save(books)
        print("상태를 바꿨습니다.")


def main():
    books = load()
    while True:
        print()
        print("[나의 독서 기록] 1) 책 추가  2) 목록  3) 검색  4) 상태 바꾸기  5) 끝내기")
        menu = input("번호를 고르세요: ").strip()
        if menu == "1":
            add(books)
        elif menu == "2":
            show(books)
        elif menu == "3":
            search(books)
        elif menu == "4":
            change_status(books)
        elif menu == "5":
            break


if __name__ == "__main__":
    main()
