from ninja import Router, Query
from django.http import HttpRequest, HttpResponse, JsonResponse
from ninja.errors import HttpError
from smrp.setup import service
from smrp.models import Pager
from smrp.dto import KeywordDto
from smrp.constant import AppConstant

router = Router(tags=["Setup/City"])

table = "city"

@router.get("/lookup/cities")
async def lookup_list(request):
    return await service.find_all(table, 0, 0, '', '')

@router.get("/cities")
async def list(request, response: HttpResponse,
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
            
    total = await service.count(table)
    pg = Pager(total, page, limit)
    lx = await service.find_all(table, pg.lower_bound, pg.page_size, sortby, sortdir)
    
    response[AppConstant.X_TOTAL_COUNT] = str(total)
    response[AppConstant.X_TOTAL_PAGE] = str(pg.total_pages)
    return lx

@router.post("/cities")
async def search_list(request, response: HttpResponse, 
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
        
    total = await service.count_by_keyword(key, table)
    pg = Pager(total, page, limit)
    lx = await service.find_by_keyword(key, pg.lower_bound, pg.page_size, sortby, sortdir, table)
    
    response[AppConstant.X_TOTAL_COUNT] = str(total)
    response[AppConstant.X_TOTAL_PAGE] = str(pg.total_pages)
    return lx

@router.get("/city/{id}")
async def edit(request, id: int):
    o = await service.find_by_id(id, table)
    if o:
        return o
    
    return JsonResponse({
        "statusCode": 404,
        "message": "Record not found"
    }, status=404)

@router.delete("/city/{id}")
async def delete(request, id: int):
    user_id = request.auth.id
    if request.auth is None:
        raise HttpError(401, "Unauthorized")
    
    await service.delete_by_id(id, user_id, table)
    return {
        "success": 1
    }