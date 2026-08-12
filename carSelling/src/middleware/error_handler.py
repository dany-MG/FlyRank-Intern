from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

def setup_error_handlers(app):
    @app.exception_handler(RequestValidationError)
    async def invalid_input_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=400,
            content={"message": f"Invalid input"},
        )