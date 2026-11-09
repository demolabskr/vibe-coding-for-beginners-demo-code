"""books.json의 책을 books.db로 옮긴다. 원본 books.json은 지우지 않는다."""
import json

import books_db

SOURCE = books_db.DB_FILE.with_name("books.json")


def main():
    if not SOURCE.exists():
        print("books.json이 없습니다. 옮길 책이 없습니다.")
        return
    books = json.loads(SOURCE.read_text(encoding="utf-8"))
    existing = {(row["title"], row["author"]) for row in books_db.list_books()}
    moved = 0
    for book in books:
        if (book["title"], book["author"]) in existing:
            continue
        books_db.add_book(book["title"], book["author"], book.get("status", "읽고 싶음"))
        moved += 1
    print(f"books.json {len(books)}권 가운데 {moved}권을 books.db로 옮겼습니다. 지금 books.db에는 {len(books_db.list_books())}권이 있습니다.")


if __name__ == "__main__":
    main()
