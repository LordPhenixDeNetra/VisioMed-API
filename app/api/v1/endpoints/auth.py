from typing import Annotated
from importlib import import_module
from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import ValidationError
from datetime import timedelta

from app.api import deps
from app.schemas.token import Token, TokenPayload
from app.schemas.user import UserResponse
from app.services.auth import auth_service
from app.services.user import user_service
from app.db.models.user import User
from app.core.config import settings
from app.core.security import create_access_token

jose = import_module("jose")
jwt = import_module("jose.jwt")
JWTError = jose.JWTError

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

@router.post("/refresh-token", response_model=Token)
async def refresh_token(
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    refresh_token: str = Body(..., embed=True),
) -> Token:
    """
    Refresh access token.
    """
    try:
        payload = jwt.decode(
            refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
        
    sub = token_data.sub
    if sub is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await user_service.get(db, id=int(sub))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
        
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token, 
        token_type="bearer", 
        refresh_token=refresh_token # Return same refresh token (rotation logic can be added later)
    )

@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: Annotated[User, Depends(deps.get_current_active_user)]
) -> User:
    """
    Get current user.
    """
    return current_user
