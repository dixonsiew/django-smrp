from ninja_extra import NinjaExtraAPI
from smrp.controllers.setup.city import CityController


def register_route(api: NinjaExtraAPI):
    api.register_controllers(CityController)