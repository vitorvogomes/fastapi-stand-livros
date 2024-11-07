import sqlite3

def create_database():
    with sqlite3.connect("./db_main/books.db") as db:
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS BooksData
            (id INTEGER PRIMARY KEY, nome TEXT, autor TEXT, valor FLOAT, categoria TEXT)
        """)
        db.commit()

        