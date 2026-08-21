import sqlite3
from datetime import datetime, date
from render import generate_pdf_report
from src.models.report_models import ReportRequest
from fastapi.responses import JSONResponse

def create_report(req: ReportRequest = ReportRequest()):
    conn = sqlite3.connect('report.db')
    cursor = conn.cursor()

    if not req.force:
        today_date = date.today().isoformat()
        cursor.execute("SELECT id FROM reports WHERE created_at LIKE ?", (f"{today_date}%",))
        existing_report = cursor.fetchone()

        if existing_report:
            conn.close()
            return JSONResponse(
                status_code = 200,
                content={
                    "id": existing_report[0],
                    "file": f"/reports/{existing_report[0]}/file"
                }
            )

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
