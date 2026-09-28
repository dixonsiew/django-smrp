from ninja import NinjaAPI, Swagger
from ninja.errors import ValidationError
from datetime import datetime, timedelta, timezone
from django.conf import settings
from django.http import HttpResponse
from .models import LoginDto, CommonSetup
from .db import pool
from .auth import jwt_auth

import logging, jwt, datetime

logger = logging.getLogger(__name__)

api = NinjaAPI(auth=jwt_auth, docs=Swagger(settings={"persistAuthorization": True}))


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

@api.post("/login", auth=None)
def login(request, data: LoginDto, response: HttpResponse):
    payload = {
        "sub": '8',
        "username": "admin",
        "exp": datetime.datetime.now(timezone.utc) + timedelta(hours=720)
    }
    payloadr = {
        "sub": '8',
        "username": "admin",
        "exp": datetime.datetime.now(timezone.utc) + timedelta(hours=87600)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    refresh_token = jwt.encode(payloadr, settings.SECRET_KEY, algorithm="HS256")
    
    response.set_cookie(
        key="token",
        value=token,
        max_age=30 * 24 * 60 * 60,       # Expires in 1 hour (in seconds)
        httponly=True,      # Protects against XSS attacks
        secure=False,        # Only sent over HTTPS
        samesite="Lax",      # Protects against CSRF
        path="/"
    )
    response.set_cookie(
        key="refreshToken",
        value=refresh_token,
        max_age=3650 * 24 * 60 * 60,       # Expires in 1 hour (in seconds)
        httponly=True,      # Protects against XSS attacks
        secure=False,        # Only sent over HTTPS
        samesite="Lax",      # Protects against CSRF
        path="/smrp/o/refresh-token"
    )
    
    return {
        "type": "bearer",
        "token": token,
        "refresh_token": refresh_token
    }

@api.get("/city/list")
async def list_city(request):
    table = 'city'
    async with pool.acquire() as conn:
        rows = await conn.fetch(f"""
            select t.id, t.code, t.desc, t.ref, t.created_by, t.created_date, t.modified_by, t.modified_date, t.deleted, t.deleted_by, t.deleted_date 
            from {table} t where t.desc <> '' and t.deleted is not true order by t.code
        """)
    return [CommonSetup(**dict(row)) for row in rows]