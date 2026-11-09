"""독서 기록의 데이터 코드: SQLite 파일 books.db를 다룬다.

화면 코드(cli.py, gui.py)는 이 파일의 함수만 부른다.
"""
import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).parent / "books.db"
STATUSES = ["읽고 싶음", "읽는 중", "다 읽음"]


def connect():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute(
        """CREATE TABLE IF NOT EXISTS books (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               title TEXT NOT NULL,
               author TEXT NOT NULL DEFAULT '',
               status TEXT NOT NULL DEFAULT '읽고 싶음'
           )"""
    )
    return conn


def add_book(title, author, status="읽고 싶음"):
    with connect() as conn:
        conn.execute("INSERT INTO books (title, author, status) VALUES (?, ?, ?)", (title, author, status))


def list_books():
    with connect() as conn:
        return conn.execute("SELECT * FROM books ORDER BY id").fetchall()


def search_books(word):
    with connect() as conn:
        like = f"%{word}%"
        return conn.execute(
            "SELECT * FROM books WHERE title LIKE ? OR author LIKE ? ORDER BY id", (like, like)
        ).fetchall()


def set_status(book_id, status):
    with connect() as conn:
        conn.execute("UPDATE books SET status = ? WHERE id = ?", (status, book_id))


def delete_book(book_id):
    with connect() as conn:
        conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
