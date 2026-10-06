from ninja_extra import NinjaExtraAPI
from smrp.controllers.setup.adm_status import AdmStatusController
from smrp.controllers.setup.city import CityController
from smrp.controllers.setup.country import CountryController
from smrp.controllers.setup.delivery_type import DeliveryTypeController
from smrp.controllers.setup.diag_item_type import DiagItemTypeController
from smrp.controllers.setup.discharge_officer import DischargeOfficerController
from smrp.controllers.setup.discharge_type import DischargeTypeController
from smrp.controllers.setup.education import EducationController
from smrp.controllers.setup.ethnic_group import EthnicGroupController
from smrp.controllers.setup.gender import GenderController
from smrp.controllers.setup.id_type import IdTypeController
from smrp.controllers.setup.income import IncomeController
from smrp.controllers.setup.marital_status import MaritalStatusController
from smrp.controllers.setup.occupation import OccupationController
from smrp.controllers.setup.person_category_code import PersonCategoryCodeController
from smrp.controllers.setup.referral import ReferralController
from smrp.controllers.setup.relationship import RelationshipController
from smrp.controllers.setup.religion import ReligionController
from smrp.controllers.setup.speciality import SpecialityController
from smrp.controllers.setup.state import StateController
from smrp.controllers.setup.title import TitleController
from smrp.controllers.setup.visit_type import VisitTypeController
from smrp.controllers.setup.ward_class import WardClassController
from smrp.controllers.setup.user import UserController
from smrp.controllers.setup.role import RoleController


def register_route(api: NinjaExtraAPI):
    api.register_controllers(AdmStatusController)
    api.register_controllers(CityController)
    api.register_controllers(CountryController)
    api.register_controllers(DeliveryTypeController)
    api.register_controllers(DiagItemTypeController)
    api.register_controllers(DischargeOfficerController)
    api.register_controllers(DischargeTypeController)
    api.register_controllers(EducationController)
    api.register_controllers(EthnicGroupController)
    api.register_controllers(GenderController)
    api.register_controllers(IdTypeController)
    api.register_controllers(IncomeController)
    api.register_controllers(MaritalStatusController)
    api.register_controllers(OccupationController)
    api.register_controllers(PersonCategoryCodeController)
    api.register_controllers(ReferralController)
    api.register_controllers(RelationshipController)
    api.register_controllers(ReligionController)
    api.register_controllers(SpecialityController)
    api.register_controllers(StateController)
    api.register_controllers(TitleController)
    api.register_controllers(VisitTypeController)
    api.register_controllers(WardClassController)
    
    api.register_controllers(UserController)
    api.register_controllers(RoleController)