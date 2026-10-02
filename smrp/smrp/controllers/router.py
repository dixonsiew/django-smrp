from ninja_extra import NinjaExtraAPI
from .auth.router import register_route as register_auth_route
from .setup.router import register_route as register_setup_route
from .report.router import register_route as register_report_route


def register_route(api: NinjaExtraAPI):
    register_auth_route(api)
    register_setup_route(api)
    register_report_route(api)