from ninja_extra import NinjaExtraAPI
from smrp.controllers.report.master_pd101.master_pd101 import MasterPD101Controller
from smrp.controllers.report.master_pd102.master_pd102 import MasterPD102Controller
from smrp.controllers.report.master_pd105.master_pd105 import MasterPD105Controller
from smrp.controllers.report.master_pd301.master_pd301 import MasterPD301Controller


def register_route(api: NinjaExtraAPI):
    api.register_controllers(MasterPD101Controller)
    api.register_controllers(MasterPD102Controller)
    api.register_controllers(MasterPD105Controller)
    api.register_controllers(MasterPD301Controller)