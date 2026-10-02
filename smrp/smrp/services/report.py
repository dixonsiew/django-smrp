from smrp.constant import AppConstant
from smrp.services.common_setup import CommonSetupService
from injector import inject


class ReportService:
    
    @inject
    def __init__(self, cs: CommonSetupService):
        self.cs = cs
        
    async def ref_referral_source_code(self, doc):
        return await self.get_code("REFERRAL", doc, "referral")

    async def ref_person_title_code(self, doc):
        return await self.get_code("TITLE", doc, "title")

    async def ref_gender_code(self, doc):
        return await self.get_code("GENDER", doc, "gender")

    async def ref_gender_code_1(self, doc):
        return await self.get_code("CHILD_SEX", doc, "gender")

    async def ref_marital_status_code(self, doc):
        return await self.get_code("MARITAL_STATUS", doc, "marital_status")

    async def ref_religion_code(self, doc):
        return await self.get_code("RELIGION", doc, "religion")

    async def ref_citizenship_code(self, doc):
        return await self.get_code("NATIONALITY", doc, "country")

    async def ref_citizenship_code_nok(self, doc):
        return await self.get_code("NOK_NATIONALITY", doc, "country")

    async def ref_ethnic_code(self, doc):
        return await self.get_code("ETHNIC_GROUP", doc, "ethnic_group")

    async def ref_foreigner_origin_country_code(self, doc):
        return await self.get_code("COUNTRY_OF_BIRTH", doc, "country")

    async def ref_foreigner_residence_country_code(self, doc):
        return await self.get_code("REFFOREIGNRCOUNTRYCODE", doc, "country")

    async def ref_person_category_code(self, doc):
        return await self.get_code("REFPERSONCATEGORYCODE", doc, "person_category_code")

    async def ref_identification_type_code(self, doc):
        return await self.get_code("DOCUMENT_TYPE", doc, "id_type")

    async def ref_city_code(self, doc):
        return await self.get_code("CITYCODE", doc, "city")

    async def ref_city_code_nok(self, doc):
        return await self.get_code("NOK_CITYCODE", doc, "city")

    async def ref_state_code(self, doc):
        return await self.get_code("OCITY", doc, "state")

    async def ref_state_code_nok(self, doc):
        return await self.get_code("NOK_OCITY", doc, "state")

    async def ref_person_title_code_nok(self, doc):
        return await self.get_code("NOK_TITLE", doc, "title")

    async def ref_relationship_code(self, doc):
        return await self.get_code("RELATION_DESCRIPTION", doc, "relationship")

    async def ref_identification_type_code_nok(self, doc):
        return await self.get_code("NOK_ID_TYPE", doc, "id_type")

    async def ref_discipline_code(self, doc):
        return await self.get_code("PRIMARY_SPECIALITY", doc, "speciality")

    async def ref_discipline_code_1(self, doc):
        return await self.get_code("PRIMARY_SPECIALTY", doc, "speciality")

    async def ref_ward_class_code(self, doc):
        return await self.get_code("PAYMENT_CLASS_CODE", doc, "ward_class")
        
    async def ref_discharge_type_code(self, doc):
        return await self.get_code("DISCHARGE_REASON", doc, "discharge_type")

    async def ref_diagnosis_item_type_code(self, doc):
        return await self.get_code("DIAGNOSIS_DESC", doc, "diag_item_type")
    
    async def ref_labour_mode_code(self, doc):
        return await self.get_code("DELIVERY_TYPE", doc, "delivery_type")
    
    async def get_code(self, key, doc, table):
        x = AppConstant.NO_INFO
        s = self.get(key, doc)
        if s != "":
            try:
                o = await self.cs.find_by_desc(s, table)
                if o is not None:
                    x = o.code
                    
            except:
                pass
            
        return x
    
    def get(self, key, doc):
        s = ""
        if key in doc:
            s = str(doc[key])
            s = s.strip()
            
        return s