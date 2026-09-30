from ninja import Query
from django.http import JsonResponse
from ninja.errors import HttpError
from ninja_extra import api_controller, http_get, http_post, http_put, http_delete

from smrp.services.role import RoleService
from smrp.services.user import UserServie
from smrp.models import Pager
from smrp.dto import KeywordDto, UserDto
from smrp.constant import AppConstant


@api_controller('/api', tags=['Setup/User'])
class UserController:
    
    def __init__(self, role_service: RoleService, service: UserServie):
        self.service = service
        self.role_service = role_service
        
    @http_get("/users")
    async def list(self, 
                   page: int = Query('1', alias='_page'),
                   limit: int = Query('20', alias='_limit'),
                   sort: str = ""):
        sorts = sort
        
        sortby = "username"
        sortdir = "asc"
        
        if sorts != "":
            lis = sorts.split("$")
            s = lis[0]
            arr = s.split(":")
            sortby = arr[0]
            sortdir = arr[1]
            
        total = await self.service.count()
        pg = Pager(total, int(page), int(limit))
        lx = await self.service.find_all(pg.lower_bound, pg.page_size, sortby, sortdir)
        
        self.context.response.headers[AppConstant.X_TOTAL_COUNT] = str(total)
        self.context.response.headers[AppConstant.X_TOTAL_PAGE] = str(pg.total_pages)
        return lx
    
    @http_post("/users")
    async def search_list(self,
                          keyword: KeywordDto,
                          page: int = Query('1', alias='_page'),
                          limit: int = Query('20', alias='_limit'),
                          sort: str = ""):
        sorts = sort
        sortby = "username"
        sortdir = "asc"

        data = keyword
        key = f'%{data.keyword}%'

        if sorts != "":
            lis = sorts.split("$")
            s = lis[0]
            arr = s.split(":")
            sortby = arr[0]
            sortdir = arr[1]

        total = await self.service.count_by_keyword(key)
        pg = Pager(total, int(page), int(limit))
        lx = await self.service.find_by_keyword(key, pg.lower_bound, pg.page_size, sortby, sortdir)
        
        self.context.response.headers[AppConstant.X_TOTAL_COUNT] = str(total)
        self.context.response.headers[AppConstant.X_TOTAL_PAGE] = str(pg.total_pages)
        return lx
    
    @http_post("/user")
    async def create(self, data: UserDto):
        user_id = self.context.request.auth.id
        if user_id is None:
            raise HttpError(401, "Unauthorized")

        b = await self.service.exists_by_username(data.username)
        
        if b:
            return self.bad_request({
                "statusCode": 400,
                "message": "A user with that username already exists"
            })
            
        role = await self.role_service.find_by_id(data.role_id)
        
        if role is None:
            return JsonResponse({
                "statusCode": 404,
                "message": "A user with that username already exists"
            }, status=404)
            
        # o = User(password=data.password, username=data.username, first_name=data.first_name, last_name=data.last_name, roles=[role])
        # await self.cs.save(o)
        return {
            "success": 1
        }