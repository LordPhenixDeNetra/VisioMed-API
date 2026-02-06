from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, refs, actes, reports

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(refs.router, prefix="/refs", tags=["References"])
api_router.include_router(actes.router, prefix="/actes", tags=["Medical Acts"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
