from typing import List, Optional
from datetime import date
from pydantic import BaseModel, Field

class Period(BaseModel):
    start: date
    end: date

class RevenueByService(BaseModel):
    service: str
    acts: int
    montant: float

class RevenueByType(BaseModel):
    type: str
    acts: int
    montant: float

class RevenueByMedecin(BaseModel):
    medecin: str
    acts: int
    montant: float

class FinancialSummaryResponse(BaseModel):
    period: Period
    total_revenue: float
    total_acts: int
    by_service: List[RevenueByService] = Field(default_factory=list)
    by_type: List[RevenueByType] = Field(default_factory=list)
    by_medecin: List[RevenueByMedecin] = Field(default_factory=list)
