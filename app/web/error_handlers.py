from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.domain.exceptions.domain_exceptions import (
    DomainException,
    EntityNotFoundError,
    EntityAlreadyExistsError,
    InvalidPolymorphicDetailsError,
    BusinessRuleConflictError,
)


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(EntityNotFoundError)
    async def entity_not_found_handler(request: Request, exc: EntityNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": exc.message, "error": "NOT_FOUND"},
        )

    @app.exception_handler(EntityAlreadyExistsError)
    async def entity_already_exists_handler(request: Request, exc: EntityAlreadyExistsError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": exc.message, "error": "CONFLICT"},
        )

    @app.exception_handler(InvalidPolymorphicDetailsError)
    async def invalid_details_handler(request: Request, exc: InvalidPolymorphicDetailsError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exc.message, "error": "INVALID_POLYMORPHIC_STRUCTURE"},
        )

    @app.exception_handler(BusinessRuleConflictError)
    async def business_conflict_handler(request: Request, exc: BusinessRuleConflictError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": exc.message, "error": "BUSINESS_RULE_VIOLATION"},
        )

    @app.exception_handler(DomainException)
    async def generic_domain_handler(request: Request, exc: DomainException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": exc.message, "error": "DOMAIN_ERROR"},
        )
