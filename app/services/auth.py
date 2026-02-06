from datetime import timedelta
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.core.security import verify_password, create_access_token, create_refresh_token
from app.core.config import settings
from app.schemas.token import Token
from app.db.models.user import User
from app.services.user import user_service

class AuthService:
    async def authenticate_user(
        self, db: AsyncSession, username_or_email: str, password: str
    ) -> Optional[User]:
        """
        Authenticate a user by username or email and password.
        """
        # Try to find by email first
        user = await user_service.get_by_email(db, email=username_or_email)
        
        # If not found, try by username
        if not user:
            user = await user_service.get_by_username(db, username=username_or_email)
            
        if not user:
            return None
            
        if not verify_password(password, user.password_hash):
            return None
            
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
            
        return user

    async def login(self, db: AsyncSession, username_or_email: str, password: str) -> Token:
        """
        Login user and return access token.
        """
        user = await self.authenticate_user(db, username_or_email, password)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username/email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            subject=user.id, expires_delta=access_token_expires
        )
        
        refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        refresh_token = create_refresh_token(
            subject=user.id, expires_delta=refresh_token_expires
        )
        
        # TODO: Store refresh token in database (RefreshToken table) for revocation support
        
        return Token(
            access_token=access_token, 
            token_type="bearer",
            refresh_token=refresh_token
        )

auth_service = AuthService()
