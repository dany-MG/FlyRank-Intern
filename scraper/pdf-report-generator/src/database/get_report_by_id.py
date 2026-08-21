import sqlite3

def get_report_by_id(report_id: int):
    conn = sqlite3.connect("report.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT id, path, created_at FROM reports WHERE id = ?", (report_id,))
    report = cursor.fetchone()
    conn.close()

    if report:
        return {
            "id": report["id"],
            "path": report["path"],
            "created_at": report["created_at"]
        }
    else:
        return None

def get_report_path(report_id : int):
    conn = sqlite3.connect("report.db")
    cursor = conn.cursor()

    cursor.execute("SELECT path FROM reports WHERE id = ?", (report_id,))
    report = cursor.fetchone()
    conn.close()

    if report:
        return report[0]
    else:
        return None