"""Domain exceptions for business logic and validation."""


class DomainException(Exception):
    """Base exception for all domain errors."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class EntityNotFoundError(DomainException):
    """Raised when an entity is not found in the catalog."""
    pass


class EntityAlreadyExistsError(DomainException):
    """Raised when trying to register an entity with an existing ID."""
    pass


class InvalidPolymorphicDetailsError(DomainException):
    """Raised when the polymorphic details do not match category requirements."""
    pass


class BusinessRuleConflictError(DomainException):
    """Raised when a business rule prevents an operation (e.g., deleting an artist with works)."""
    pass
