import sqlite3
import json

def get_report_data():
    conn = sqlite3.connect("report.db")
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    cursor = conn.cursor()

    # Total books
    cursor.execute('''
        SELECT COUNT(*) as total FROM books
    ''')
    total_books = cursor.fetchone()["total"]

    # Average price
    cursor.execute('''
        SELECT AVG(price_gbp) as average_price FROM books
    ''')
    average_price = round(cursor.fetchone()["average_price"], 2)

    # Top 5 Expensive Books
    cursor.execute('''
        SELECT title, price_gbp FROM books ORDER BY price_gbp DESC LIMIT 5
    ''')
    top_5_expensive = [dict(row) for row in cursor.fetchall()]

    # Number of books per star rating
    cursor.execute('''
        SELECT rating, COUNT(*) FROM books GROUP BY rating ORDER BY rating DESC
    ''')
    count_per_rating = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return {
        "total_books": total_books,
        "average_price": average_price,
        "top_5_expensive": top_5_expensive,
        "books_per_rating": count_per_rating
    }

if __name__ == "__main__":
    report = get_report_data()
    print(json.dumps(report, indent=2))
