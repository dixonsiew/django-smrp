from ninja import NinjaAPI, Swagger
from ninja.errors import ValidationError
from .models import LoginDto

import logging

logger = logging.getLogger(__name__)

api = NinjaAPI(docs=Swagger(settings={"persistAuthorization": True}))


@api.exception_handler(Exception)
def global_exception_handler(request, exc):
    logger.exception(str(exc))
    return api.create_response(
        request,
        {"message": "Internal Server Error", "detail": str(exc)},
        status=500
    )


@api.exception_handler(ValidationError)
def custom_validation_error_handler(request, exc: ValidationError):
    # exc.errors contains a list of dicts with error details (location, message, type)
    errs = exc.errors
    lm = []
    for err in errs:
        s = ".".join(str(loc) for loc in err["loc"])
        ms = err["msg"]
        lm.append(f"[{s}] {ms}")
        
    return api.create_response(
        request,
        {
            "statusCode": 422,
            "message": " and ".join(lm),
            # "errors": exc.errors,
        },
        status=422,  # Change to 400 if you prefer Bad Request
    )


@api.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}

@api.post("/login")
def login(request, data: LoginDto):
    return data