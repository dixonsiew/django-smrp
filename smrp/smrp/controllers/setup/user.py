from ninja import Query
from ninja_extra import api_controller, http_get, http_post, http_put, http_delete

from smrp.services.role import RoleService
from smrp.services.user import UserServie
from smrp.models import Pager


@api_controller('/api', tags=['Setup/User'])
class UserController:
    
    def __init__(self, role_service: RoleService, service: UserServie):
        self.service = service
        self.role_service = role_service
        
    @http_get("/users")
    async def list(self, 
                   page: int = Query(1, alias='_page'),
                    _limit: FromQuery[int] = FromQuery(20),
                    sort: FromQuery[str] = FromQuery(""),
    ) -> List[User]:
        page = _page.value
        limit = _limit.value
        sorts = sort.value
        
        sortby = "username"
        sortdir = "asc"
        
        if sorts != "":
            lis = sorts.split("$")
            s = lis[0]
            arr = s.split(":")
            sortby = arr[0]
            sortdir = arr[1]
            
        total = await self.cs.count()
        pg = Pager(total, page, limit)
        lx = await self.cs.find_all(offset=pg.lower_bound, limit=pg.page_size, sortby=sortby, sortdir=sortdir)
        ly = [x.to_dict() for x in lx]
        res = self.json(ly)
        res.headers.add(AppConstant.X_TOTAL_COUNT, bytes(str(total), 'utf-8'))
        res.headers.add(AppConstant.X_TOTAL_PAGE, bytes(str(pg.total_pages), 'utf-8'))
        return res