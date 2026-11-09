"""독서 기록 데스크톱 앱(tkinter): 같은 books.db를 창과 버튼으로 다룬다."""
import tkinter as tk
from tkinter import messagebox, ttk

import books_db


class BookApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("나의 독서 기록")
        self.geometry("560x420")

        form = ttk.Frame(self, padding=10)
        form.pack(fill="x")
        ttk.Label(form, text="제목").grid(row=0, column=0, sticky="w")
        self.title_entry = ttk.Entry(form, width=30)
        self.title_entry.grid(row=0, column=1, padx=5)
        ttk.Label(form, text="저자").grid(row=1, column=0, sticky="w")
        self.author_entry = ttk.Entry(form, width=30)
        self.author_entry.grid(row=1, column=1, padx=5)
        self.status_box = ttk.Combobox(form, values=books_db.STATUSES, state="readonly", width=10)
        self.status_box.current(0)
        self.status_box.grid(row=0, column=2, padx=5)
        ttk.Button(form, text="등록", command=self.add).grid(row=1, column=2, padx=5)

        search = ttk.Frame(self, padding=(10, 0))
        search.pack(fill="x")
        self.search_entry = ttk.Entry(search, width=30)
        self.search_entry.pack(side="left")
        ttk.Button(search, text="검색", command=self.refresh).pack(side="left", padx=5)

        self.table = ttk.Treeview(self, columns=("title", "author", "status"), show="headings")
        for key, label in (("title", "제목"), ("author", "저자"), ("status", "상태")):
            self.table.heading(key, text=label)
        self.table.pack(fill="both", expand=True, padx=10, pady=10)
        self.refresh()

    def add(self):
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showwarning("알림", "제목은 꼭 입력해 주세요.")
            return
        books_db.add_book(title, self.author_entry.get().strip(), self.status_box.get())
        self.title_entry.delete(0, "end")
        self.author_entry.delete(0, "end")
        self.refresh()

    def refresh(self):
        word = self.search_entry.get().strip()
        rows = books_db.search_books(word) if word else books_db.list_books()
        self.table.delete(*self.table.get_children())
        for row in rows:
            self.table.insert("", "end", values=(row["title"], row["author"], row["status"]))


if __name__ == "__main__":
    BookApp().mainloop()
