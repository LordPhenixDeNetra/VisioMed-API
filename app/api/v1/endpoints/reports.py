from typing import Annotated, Any
from datetime import date
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.services.report import report_service
from app.services.export import export_service
from app.db.models.user import User

router = APIRouter()

@router.get("/financial-summary")
async def get_financial_summary(
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    start_date: date = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: date = Query(..., description="End date (YYYY-MM-DD)"),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get financial summary for the specified period.
    """
    return await report_service.get_financial_summary(db, start_date, end_date)

@router.get("/export/excel")
async def export_excel(
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    start_date: date,
    end_date: date,
    current_user: User = Depends(deps.get_current_active_user),
):
    """
    Export medical acts to Excel.
    """
    # TODO: Fetch real data from ActeService filtering by date
    # For now, demo data
    data = [
        {"Date": "2023-01-01", "Patient": "John Doe", "Montant": 10000},
        {"Date": "2023-01-02", "Patient": "Jane Doe", "Montant": 15000},
    ]
    
    file_stream = export_service.generate_excel(data)
    
    headers = {
        'Content-Disposition': f'attachment; filename="rapport_{start_date}_{end_date}.xlsx"'
    }
    return StreamingResponse(file_stream, headers=headers, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
