from ninja_extra import api_controller, http_get, http_post, http_put, http_delete

from smrp.services.role import RoleService


@api_controller('/api', tags=['Setup/Role'])
class RoleController:
    
    def __init__(self, service: RoleService):
        self.service = service
            
    @http_get("/lookup/groups")
    async def lookup_list(self):
        return await self.service.find_all("name", "asc")