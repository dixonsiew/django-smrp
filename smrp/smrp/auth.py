import jwt
from django.conf import settings
from django.http import HttpRequest
from ninja.security.base import AuthBase
from smrp.models import AuthUser


class JWTAuthBearer(AuthBase):
    openapi_type: str = "http"
    
    def __call__(self, request: HttpRequest):
        token = request.headers.get("Authorization")
        if not token:
            token = request.COOKIES.get("token", "")
            
        if token in [None, ""]:
            return None
            
        if token.startswith("Bearer "):
            token = token.split(" ")[1]
            
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("sub")
            username = payload.get("username")
            
            if not user_id:
                return None
            
            o = AuthUser(id=int(user_id), username=username, first_name='sys admin')
            return o
            
        except Exception as e:
            return None
        
jwt_auth = JWTAuthBearer()