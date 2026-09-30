from datetime import datetime, timedelta, timezone
from django.conf import settings
from smrp.models import User
import jwt


class TokenService:
    
    def get_token(self, id: int, username: str) -> str:
        payload = {
            "sub": str(id),
            "username": username,
            "exp": datetime.now(timezone.utc) + timedelta(hours=720)
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return token
        
    def get_refresh_token(self, id: int, username: str) -> str:
        payload = {
            "sub": str(id),
            "username": username,
            "exp": datetime.now(timezone.utc) + timedelta(hours=87600)
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return token
    
    def get_token_from_refresh(self, refresh_token: str):
        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
            username = payload.get("username")
            sub = payload.get("sub")
            o = {
                "sub": sub,
                "username": username,
                "exp": datetime.now(timezone.utc) + timedelta(hours=720)
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
            r = {
                "sub": sub,
                "username": username,
                "exp": datetime.now(timezone.utc) + timedelta(hours=87600)
            }
            rtoken = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
            return {
                "token": token,
                "refresh_token": rtoken
            }
            
        except Exception:
            return None