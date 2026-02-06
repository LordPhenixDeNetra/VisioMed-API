from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.schemas.token import Token
from app.schemas.user import UserResponse
from app.services.auth import auth_service
from app.services.user import user_service
from app.db.models.user import User

router = APIRouter()

@router.post("/login", response_model=Token)
async def login_access_token(
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    return await auth_service.login(
        db, username_or_email=form_data.username, password=form_data.password
    )

@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: Annotated[User, Depends(deps.get_current_active_user)]
) -> User:
    """
    Get current user.
    """
    return current_user
