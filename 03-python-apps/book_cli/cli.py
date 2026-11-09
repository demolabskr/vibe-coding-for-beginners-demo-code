"""독서 기록 프로그램 SQLite판: 메뉴와 동작은 JSON판과 같고 저장소만 바뀌었다."""
import books_db


def show(rows):
    if not rows:
        print("  (책이 없습니다)")
    for row in rows:
        print(f"  {row['id']}. {row['title']} / {row['author']} [{row['status']}]")


def main():
    while True:
        print()
        print("[나의 독서 기록] 1) 책 추가  2) 목록  3) 검색  4) 상태 바꾸기  5) 끝내기")
        menu = input("번호를 고르세요: ").strip()
        if menu == "1":
            title = input("제목: ").strip()
            author = input("저자: ").strip()
            if title:
                books_db.add_book(title, author)
                print(f"'{title}'을(를) 등록했습니다.")
            else:
                print("제목은 꼭 입력해 주세요.")
        elif menu == "2":
            show(books_db.list_books())
        elif menu == "3":
            show(books_db.search_books(input("찾을 말(제목이나 저자): ").strip()))
        elif menu == "4":
            show(books_db.list_books())
            book_id = input("상태를 바꿀 책 번호: ").strip()
            choice = input("1) 읽고 싶음  2) 읽는 중  3) 다 읽음: ").strip()
            if book_id.isdigit() and choice in ("1", "2", "3"):
                books_db.set_status(int(book_id), books_db.STATUSES[int(choice) - 1])
                print("상태를 바꿨습니다.")
        elif menu == "5":
            break


if __name__ == "__main__":
    main()
