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

@router.post("/login", response_model=Token, summary="Connexion utilisateur", description="Authentifie un utilisateur via OAuth2 (username/password) et retourne un token d'accès JWT ainsi qu'un refresh token.")
async def login_access_token(
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    **Description détaillée :**
    Cet endpoint permet à un utilisateur de se connecter en fournissant son nom d'utilisateur (ou email) et son mot de passe.
    
    **Paramètres :**
    - `username` : Nom d'utilisateur ou email.
    - `password` : Mot de passe de l'utilisateur.
    
    **Réponse :**
    - `access_token` : Jeton JWT pour l'authentification des requêtes futures.
    - `token_type` : Type de jeton (généralement "bearer").
    - `refresh_token` : Jeton permettant d'obtenir un nouveau token d'accès sans se reconnecter.
    """
    return await auth_service.login(
        db, username_or_email=form_data.username, password=form_data.password
    )

@router.post("/refresh-token", response_model=Token, summary="Rafraîchir le token", description="Génère un nouveau token d'accès à partir d'un refresh token valide.")
async def refresh_token(
    db: Annotated[AsyncSession, Depends(deps.get_db)],
    refresh_token: str = Body(..., embed=True, description="Le refresh token obtenu lors de la connexion"),
) -> Token:
    """
    **Description détaillée :**
    Permet de renouveler le token d'accès (access token) lorsque celui-ci est expiré, sans obliger l'utilisateur à ressaisir ses identifiants.
    
    **Paramètres :**
    - `refresh_token` : Le token de rafraîchissement actuel.
    
    **Réponse :**
    - Un nouvel `access_token` et le `refresh_token` (qui peut être le même ou un nouveau selon la politique de rotation).
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

@router.get("/me", response_model=UserResponse, summary="Profil utilisateur courant", description="Récupère les informations détaillées de l'utilisateur actuellement connecté.")
async def read_users_me(
    current_user: Annotated[User, Depends(deps.get_current_active_user)]
) -> User:
    """
    **Description détaillée :**
    Retourne l'objet utilisateur complet correspondant au token JWT fourni dans l'en-tête Authorization.
    
    **Permissions :**
    - Nécessite un token d'accès valide.
    - L'utilisateur doit être actif.
    
    **Réponse :**
    - Informations de l'utilisateur (id, email, nom, rôles, etc.).
    """
    return current_user
