from ninja_extra import api_controller, http_get, http_post
from datetime import datetime, timedelta, timezone
from django.conf import settings
import jwt

@api_controller('/', tags=['Auth'])
class AuthController:
    
    @http_post("/o/token", auth=None)
    def login(self):
        payload = {
            "sub": '8',
            "username": "admin",
            "exp": datetime.now(timezone.utc) + timedelta(hours=720)
        }
        payloadr = {
            "sub": '8',
            "username": "admin",
            "exp": datetime.now(timezone.utc) + timedelta(hours=87600)
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        refresh_token = jwt.encode(payloadr, settings.SECRET_KEY, algorithm="HS256")
        
        self.context.response.set_cookie(
            key="token",
            value=token,
            max_age=30 * 24 * 60 * 60,       # Expires in 1 hour (in seconds)
            httponly=True,      # Protects against XSS attacks
            secure=False,        # Only sent over HTTPS
            samesite="Lax",      # Protects against CSRF
            path="/"
        )
        self.context.response.set_cookie(
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