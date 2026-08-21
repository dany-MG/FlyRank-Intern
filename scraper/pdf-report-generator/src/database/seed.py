import sqlite3
import json

def seed_database():
    conn = sqlite3.connect('report.db')
    cursor = conn.cursor()

    rating_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    #Create tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    price_gbp REAL,
    rating INTEGER,
    product_url TEXT
    )'''
    )

    # Avoiding duplicate entries by clearing the table before seeding
    cursor.execute('''DELETE FROM books''')

    with open('src/output/books.json', 'r', encoding = 'utf-8') as f:
        books = json.load(f)

    for book in books:
        rating_str = book.get('rating_text')
        rating_value = rating_map.get(rating_str, 0)  # Default to 0 if not found
        cursor.execute('''INSERT INTO books (title, price_gbp, rating, product_url) VALUES (?, ?, ?, ?)''',
                       (book.get('title'), book.get('price_gbp'), rating_value, book.get('product_url')))
    
    conn.commit()

    cursor.execute('''SELECT COUNT(*) FROM books''')
    count = cursor.fetchone()[0]

    print(f"Seeded {count} books into the database.")

    conn.close()

if __name__ == '__main__':
    seed_database()