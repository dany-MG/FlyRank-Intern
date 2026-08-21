from fastapi import APIRouter, status, HTTPException
from src.database.create_reports import create_report
from src.database.get_report_by_id import get_report_by_id, get_report_path
from fastapi.responses import FileResponse

router = APIRouter(tags=["Report Routes"])

@router.post("/reports", status_code = status.HTTP_201_CREATED)
def generate_report():
    report = create_report()
    return report

@router.get("/reports/{report_id}")
def get_report(report_id:int):
    report = get_report_by_id(report_id)
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    
    return {
        "id": report["id"],
        "file": f"/reports/{report['id']}/file",
        "created_at": report["created_at"]
    }

@router.get("/reports/{report_id}/file")
def download_report(report_id: int):
    report_path = get_report_path(report_id)
    if not report_path:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report file not found")

    return FileResponse(path=report_path, media_type="application/pdf", filename=f"report_{report_id}.pdf")
