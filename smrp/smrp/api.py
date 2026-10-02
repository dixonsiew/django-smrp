from ninja import Swagger
from ninja.errors import ValidationError
from ninja_extra import NinjaExtraAPI
from .auth import jwt_auth

import logging, traceback

logger = logging.getLogger(__name__)

api = NinjaExtraAPI(auth=jwt_auth, docs=Swagger(settings={"persistAuthorization": True}))

from smrp.controllers.router import register_route


@api.exception_handler(Exception)
def global_exception_handler(request, exc):
    logger.error(traceback.format_exc())
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
   
register_route(api)