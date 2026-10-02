from ninja_extra import NinjaExtraAPI
from smrp.controllers.report.master_pd101.master_pd101 import MasterPD101Controller


def register_route(api: NinjaExtraAPI):
    api.register_controllers(MasterPD101Controller)