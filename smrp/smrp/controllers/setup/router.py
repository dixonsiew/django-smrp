from ninja_extra import NinjaExtraAPI
from smrp.controllers.setup.city import CityController
from smrp.controllers.setup.user import UserController
from smrp.controllers.setup.role import RoleController


def register_route(api: NinjaExtraAPI):
    api.register_controllers(CityController)
    api.register_controllers(UserController)
    api.register_controllers(RoleController)