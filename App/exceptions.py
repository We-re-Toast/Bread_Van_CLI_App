class AppError(Exception):
    """Base class for other exceptions"""
    pass

class ResourceNotFound(AppError):
    """Raised when a resource is not found"""
    pass

class DuplicateEntity(AppError):
    """Raised when trying to create an entity that already exists"""
    pass

class ValidationError(AppError):
    """Raised when input validation fails"""
    pass
