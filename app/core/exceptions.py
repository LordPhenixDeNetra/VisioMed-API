from typing import Any, Dict, Optional

class AppError(Exception):
    """Base exception for application errors."""
    pass

class EntityNotFound(AppError):
    """Raised when an entity is not found in the database."""
    def __init__(self, entity_name: str, entity_id: Any = None):
        self.entity_name = entity_name
        self.entity_id = entity_id
        super().__init__(f"{entity_name} not found{f' with id {entity_id}' if entity_id else ''}")

class EntityAlreadyExists(AppError):
    """Raised when an entity already exists (unique constraint violation)."""
    def __init__(self, entity_name: str, field: str, value: Any):
        self.entity_name = entity_name
        self.field = field
        self.value = value
        super().__init__(f"{entity_name} with {field}={value} already exists")

class AuthenticationError(AppError):
    """Raised when authentication fails."""
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(detail)

class PermissionDenied(AppError):
    """Raised when user doesn't have permission."""
    def __init__(self, detail: str = "Permission denied"):
        super().__init__(detail)

class BusinessLogicError(AppError):
    """Raised when a business rule is violated."""
    def __init__(self, detail: str):
        super().__init__(detail)
