from typing import Any, Dict, Optional
from fastapi import HTTPException, status

class BaseAPIException(HTTPException):
    status_code = 500
    detail = "Une erreur serveur est survenue."

    def __init__(self, detail: Optional[str] = None, headers: Optional[Dict[str, Any]] = None):
        if detail:
            self.detail = detail
        super().__init__(status_code=self.status_code, detail=self.detail, headers=headers)

class NotFoundException(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Ressource introuvable."

class PermissionDeniedException(BaseAPIException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Vous n'avez pas les permissions nécessaires."

class AuthenticationFailedException(BaseAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Authentification échouée."
    
class BadRequestException(BaseAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Requête invalide."

class ConflictException(BaseAPIException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Conflit de données."
