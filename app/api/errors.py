from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.core.exceptions import InternalError, NoteNotFound, UserNotFound, UserCredentialsMismatch, CredentialsException

async def endpoint_internal_error_handler(request: Request, exc: InternalError):
    return JSONResponse(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal_Failed", "message": "An error ocurred, try again"}
    )

async def endpoint_note_not_found_handler(request: Request, exc: NoteNotFound):
    return JSONResponse(
        status_code = status.HTTP_404_NOT_FOUND,
        content={"error": "note_not_found", "message": str(exc)}
    )

async def endpoint_user_not_found_handler(request: Request, exc: UserNotFound):
    return JSONResponse(
        status_code = status.HTTP_404_NOT_FOUND,
        content={"error": "user_not_found", "message": str(exc)}
    )

async def login_credentials_mismatch(request: Request, exc: UserCredentialsMismatch):
    return JSONResponse(
        status_code = status.HTTP_401_UNAUTHORIZED,
        content={"error": "mismatch_credentials", "message": "Credentials don't match any registered user"}
    )

async def credentials_exceptions(request: Request, exc: CredentialsException):
    return JSONResponse(
        status_code = status.HTTP_401_UNAUTHORIZED,
        content={"error": "credentials_invalid", "message": "Could not validate credentials"}
    )

def setup_exceptions_handlers(app):
    app.add_exception_handler(InternalError, endpoint_internal_error_handler)
    app.add_exception_handler(NoteNotFound, endpoint_note_not_found_handler)
    app.add_exception_handler(UserNotFound, endpoint_user_not_found_handler)
    app.add_exception_handler(UserCredentialsMismatch, login_credentials_mismatch)
    app.add_exception_handler(CredentialsException, credentials_exceptions)

