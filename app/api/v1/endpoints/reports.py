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

@router.get(
    "/financial-summary",
    summary="Obtenir le résumé financier",
    description="Récupère un résumé financier pour une période donnée (recettes par type d'acte, total, etc.)."
)
async def get_financial_summary(
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    start_date: date = Query(..., description="Date de début (YYYY-MM-DD)"),
    end_date: date = Query(..., description="Date de fin (YYYY-MM-DD)"),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Récupère le résumé financier pour la période spécifiée.

    - **start_date**: Date de début de la période.
    - **end_date**: Date de fin de la période.
    
    Retourne les statistiques financières.
    """
    return await report_service.get_financial_summary(db, start_date, end_date)

@router.get(
    "/export/excel",
    summary="Exporter les données en Excel",
    description="Génère et télécharge un fichier Excel contenant les actes médicaux pour une période donnée."
)
async def export_excel(
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    start_date: date = Query(..., description="Date de début (YYYY-MM-DD)"),
    end_date: date = Query(..., description="Date de fin (YYYY-MM-DD)"),
    current_user: User = Depends(deps.get_current_active_user),
):
    """
    Exporte les actes médicaux en Excel.

    - **start_date**: Date de début de la période.
    - **end_date**: Date de fin de la période.
    
    Retourne un fichier Excel (.xlsx) en téléchargement.
    """
    data = await report_service.get_actes_export_data(db, start_date, end_date)
    
    file_stream = export_service.generate_excel(data)
    
    headers = {
        'Content-Disposition': f'attachment; filename="rapport_{start_date}_{end_date}.xlsx"'
    }
    return StreamingResponse(file_stream, headers=headers, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
