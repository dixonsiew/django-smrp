from ninja_extra import NinjaExtraAPI
from smrp.controllers.auth.auth import AuthController


def register_route(api: NinjaExtraAPI):
    api.register_controllers(AuthController)