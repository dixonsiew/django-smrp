from ninja_extra import api_controller, http_get, http_post
from django.http import JsonResponse
from ninja.errors import HttpError
from datetime import datetime, timedelta, UTC
from injector import inject
from smrp.dto import LoginDto, RefreshTokenDto, ChangePasswordDto
from smrp.services.token import TokenService
from smrp.services.user import UserServie


@api_controller('/', tags=['Auth'])
class AuthController:
    
    @inject
    def __init__(self, ts: TokenService, us: UserServie):
        self.token_service = ts
        self.user_service = us
        
    @http_post("/o/logout")
    async def logout(self):
        res = self.context.response
        res.set_cookie(
            'token',
            '',
            httponly=True,
            secure=False,
            samesite='Lax',
            path='/',
            expires=datetime.now(UTC) + timedelta(hours=-1)
        )
        res.set_cookie(
            'refreshToken',
            '',
            httponly=True,
            secure=False,
            samesite='Lax',
            path='/smrp/o/refresh-token',
            expires=datetime.now(UTC) + timedelta(hours=-1)
        )
        return {
            "message": "Logged out successfully"
        }
    
    @http_post("/o/token", auth=None)
    async def login(self, data: LoginDto):
        mx = {
            "statusCode": 401,
            "message": "Invalid Credentials"
        }

        user = await self.user_service.find_by_username(data.username)
        valid = False
        if user is not None:
            valid = self.user_service.validate_credentials(user, data.password)
            
        else:
            return JsonResponse(mx, status=401)
        
        if not valid:
            return JsonResponse(mx, status=401)
            
        await self.user_service.update_last_login(user.id)
        token = self.token_service.get_token(user.id, user.username)
        refresh_token = self.token_service.get_refresh_token(user.id, user.username)
        
        res = self.context.response
        res.set_cookie(
            'token',
            token,
            httponly=True,
            secure=False,
            samesite='Lax',
            path='/',
            max_age=30 * 24 * 60 * 60
        )
        res.set_cookie(
            'refreshToken',
            refresh_token,
            httponly=True,
            secure=False,
            samesite='Lax',
            path='/smrp/o/refresh-token',
            max_age=3650 * 24 * 60 * 60
        )
        return {
            "type":          "bearer",
            "token":         token,
            "refresh_token": refresh_token
        }
        
    @http_post("/o/refresh-token", auth=None)
    async def refresh(self, data: RefreshTokenDto):
        mx = {
            "statusCode": 401,
            "message": "Invalid Credentials"
        }
        
        refresh_token = self.context.request.COOKIES.get("refreshToken")
        if refresh_token is None or refresh_token == "":
            if data.refresh_token == "":
                return JsonResponse(mx, status=401)
            
            refresh_token = data.refresh_token
            
        if refresh_token is None or refresh_token == "":
            return JsonResponse(mx, status=401)
        
        m = self.token_service.get_token_from_refresh(refresh_token)
        if m is None:
            return JsonResponse(mx, status=401)
        
        token = m.get("token")
        refresh_token = m.get("refresh_token")
        res = self.context.response
        res.set_cookie(
            'token',
            token,
            httponly=True,
            secure=False,
            samesite='Lax',
            path='/',
            max_age=30 * 24 * 60 * 60
        )
        res.set_cookie(
            'refreshToken',
            refresh_token,
            httponly=True,
            secure=False,
            samesite='Lax',
            path='/smrp/o/refresh-token',
            max_age=3650 * 24 * 60 * 60
        )
        return {
            "type":          "bearer",
            "token":         token,
            "refresh_token": refresh_token
        }
        
    @http_get("/api/current-user")
    async def user_details(self):
        o = await self.user_service.find_by_id(self.context.request.auth.id)
        if o is None:
            raise HttpError(401, "Unauthorized")

        return {
            "id":         o.id,
            "username":   o.username,
            "first_name": o.first_name,
            "last_name":  o.last_name,
            "roles":      o.roles
        }
    
    @http_post("/api/change-password") 
    async def change_password(self, data: ChangePasswordDto):
        o = await self.user_service.find_by_id(self.context.request.auth.id)
        if o is None:
            raise HttpError(401, "Unauthorized")
        
        if data.password != data.confirm_password:
            return JsonResponse({
                "statusCode": 400,
                "message": "Confirm Password does not match"
            }, status=400)
        
        o.password = data.password
        await self.user_service.update_password(o)
        return {
            "success": 1
        }