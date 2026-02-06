from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt, JWTError

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.db.database import AsyncSessionLocal
from app.services.audit_log import audit_log_service

# Setup logging
setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    debug=settings.DEBUG,
)

# Set all CORS enabled origins
if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.middleware("http")
async def audit_log_middleware(request: Request, call_next):
    response = await call_next(request)

    if request.method in {"POST", "PATCH", "PUT", "DELETE"} and request.url.path.startswith(
        settings.API_V1_STR
    ):
        path = request.url.path.replace(settings.API_V1_STR, "")
        segments = [segment for segment in path.split("/") if segment]
        if segments:
            resource_type = segments[0]
            resource_id = segments[1] if len(segments) > 1 else None
            action_map = {
                "POST": "CREATE",
                "PUT": "UPDATE",
                "PATCH": "UPDATE",
                "DELETE": "DELETE",
            }
            action = action_map.get(request.method, request.method)
            user_id = None
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.replace("Bearer ", "", 1).strip()
                try:
                    payload = jwt.decode(
                        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
                    )
                    sub = payload.get("sub")
                    if sub is not None:
                        user_id = int(sub)
                except (JWTError, ValueError, TypeError):
                    user_id = None

            if response.status_code < 400:
                async with AsyncSessionLocal() as db:
                    await audit_log_service.log_action(
                        db,
                        action=action,
                        resource_type=resource_type,
                        user_id=user_id,
                        ip_address=request.client.host if request.client else None,
                        resource_id=resource_id,
                        changes=None,
                    )

    return response

@app.get("/")
async def root():
    return {"message": "Welcome to VisioMed API"}
