import sqlite3
from datetime import datetime
from render import generate_pdf_report

def create_report():
    conn = sqlite3.connect('report.db')
    cursor = conn.cursor()

    created_at = datetime.now().isoformat()
    cursor.execute("INSERT INTO reports (path, created_at) VALUES ('pending', ?)",(created_at,))
    report_id = cursor.lastrowid

    file_path = generate_pdf_report(report_id)

    cursor.execute("UPDATE reports SET path = ? WHERE id = ?", (file_path, report_id))
    conn.commit()
    conn.close()

    return {
        "id" : report_id,
        "file" : f"/reports/{report_id}/file",
        "created_at" : created_at
    }
