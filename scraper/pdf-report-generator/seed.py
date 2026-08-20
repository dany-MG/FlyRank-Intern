import sqlite3
import json

def seed_database():
    conn = sqlite3.connect('report.db')
    cursor = conn.cursor()

    #Create tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    price REAL,
    rating INTEGER,
    url TEXT
    )'''
    )

    # Avoiding duplicate entries by clearing the table before seeding
    cursor.execute('''DELETE FROM books''')

    with open('src/output/books.json', 'r', encoding = 'utf-8') as f:
        books = json.load(f)

    for book in books:
        cursor.execute('''INSERT INTO books (title, price, rating, url) VALUES (?, ?, ?, ?)''',
                       (book.get('title'), book.get('price'), book.get('rating'), book.get('url')))
    
    conn.commit()

    cursor.execute('''SELECT COUNT(*) FROM books''')
    count = cursor.fetchone()[0]

    print(f"Seeded {count} books into the database.")

    conn.close()

if __name__ == '__main__':
    seed_database()