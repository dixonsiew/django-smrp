from ninja import Query
from django.http import JsonResponse
from ninja.errors import HttpError
from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from injector import inject

from smrp.services.common_setup import CommonSetupService
from smrp.models import Pager
from smrp.dto import KeywordDto
from smrp.constant import AppConstant


@api_controller('/api', tags=['Setup/WardClass'])
class WardClassController:
    
    @inject
    def __init__(self, service: CommonSetupService):
        self.service = service
        self.table = "ward_class"
        
    @http_get("/lookup/ward-classes")
    async def lookup_list(self):
        return await self.service.find_all(self.table, 0, 0, '', '')
    
    @http_get("/ward-classes")
    async def list(self,
                   page: int = Query('1', alias='_page'), 
                   limit: int = Query('20', alias='_limit'), 
                   sort: str = ""):
        sorts = sort
            
        sortby = "code"
        sortdir = "asc"
        
        if sorts != "":
            lis = sorts.split("$")
            s = lis[0]
            arr = s.split(":")
            sortby = arr[0]
            sortdir = arr[1]
                
        total = await self.service.count(self.table)
        pg = Pager(total, int(page), int(limit))
        lx = await self.service.find_all(self.table, pg.lower_bound, pg.page_size, sortby, sortdir)
        
        self.context.response.headers[AppConstant.X_TOTAL_COUNT] = str(total)
        self.context.response.headers[AppConstant.X_TOTAL_PAGE] = str(pg.total_pages)
        return lx

    @http_post("/ward-classes")
    async def search_list(self, 
                          keyword: KeywordDto, 
                          page: int = Query('1', alias='_page'), 
                          limit: int = Query('20', alias='_limit'), 
                          sort: str = ""):
        sorts = sort
        
        sortby = "code"
        sortdir = "asc"
        
        data = keyword
        key = f'%{data.keyword}%'
        
        if sorts != "":
            lis = sorts.split("$")
            s = lis[0]
            arr = s.split(":")
            sortby = arr[0]
            sortdir = arr[1]
            
        total = await self.service.count_by_keyword(key, self.table)
        pg = Pager(total, int(page), int(limit))
        lx = await self.service.find_by_keyword(key, pg.lower_bound, pg.page_size, sortby, sortdir, self.table)
        
        self.context.response.headers[AppConstant.X_TOTAL_COUNT] = str(total)
        self.context.response.headers[AppConstant.X_TOTAL_PAGE] = str(pg.total_pages)
        return lx

    @http_get("/ward-class/{id}")
    async def edit(self, id: int):
        o = await self.service.find_by_id(id, self.table)
        if o:
            return o
        
        return JsonResponse({
            "statusCode": 404,
            "message": "Record not found"
        }, status=404)

    @http_delete("/ward-class/{id}")
    async def delete(self, id: int):
        user_id = self.context.request.auth.id
        if self.context.request.auth is None:
            raise HttpError(401, "Unauthorized")
        
        await self.service.delete_by_id(id, user_id, self.table)
        return {
            "success": 1
        }