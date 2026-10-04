from ninja import Query, Body
from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from pymongo import MongoClient
from bson.objectid import ObjectId
from injector import inject

from smrp.db import client
from smrp.models import Pager
from smrp.services.report import ReportService
from .column_map import COLUMN_MAP
import smrp.utils as utils


@api_controller("/api/master-pd101", tags=["Report/MasterPD101"])
class MasterPD101Controller:
    
    @inject
    def __init__(self, service: ReportService):
        self.service = service
        
    @http_get("/export/rpt2")
    async def jsonrh101(self, datefrom: str = "2023-01-01", dateto: str = "2024-01-01"):
        username = self.context.request.auth.username
        col = self.get_collection(client, username, "1")
        cur = col.find({})
        ls = utils.process_doc(list(cur))

        dt1 = datefrom.split("-")
        dt2 = dateto.split("-")
        ds1 = f"{dt1[2]}{dt1[1]}{dt1[0]}"
        ds2 = f"{dt2[2]}{dt2[1]}{dt2[0]}"

        forms = []
        for d in ls:
            person = {
                "refPersonTitleCode":        await self.service.ref_person_title_code(d),
                "fullName":                  utils.get_str(d["PATIENT_NAME"]),
                "refIdentificationTypeCode": await self.service.ref_identification_type_code(d),
                "identificationNo":          utils.get_str(d["DOCUMENT_NUMBER"]),
                "refAddressTypeCode":        "C",
                "street1":                   utils.get_str(d["STREET1"]),
                "street2":                   utils.get_str(d["STREET2"]),
                "refCityCode":               await self.service.ref_city_code(d),
                "refPostCode":               utils.get_str(d["POSTCODE"]),
                "refStateCode":              await self.service.ref_state_code(d),
                "refCountryCode":            await self.service.ref_citizenship_code(d),
                "refContactTypeCode":        "02",
                "contactInfo":               utils.get_str(d["HOME_PHONE"]),
            }

            nok = {
                "refPersonTitleCode":        await self.service.ref_person_title_code_nok(d),
                "fullName":                  utils.get_str(d["PATIENT_NOK_NAME"]),
                "refIdentificationTypeCode": await self.service.ref_identification_type_code_nok(d),
                "identificationNo":          utils.get_str(d["NOK_ID"]),
                "refAddressTypeCode":        "C",
                "street1":                   str(d["NOK_STREET1"]),
                "street2":                   utils.get_str(d["NOK_STREET2"]),
                "refCityCode":               await self.service.ref_city_code_nok(d),
                "refPostCode":               utils.get_str(d["NOK_POSTCODE"]),
                "refStateCode":              await self.service.ref_state_code_nok(d),
                "refCountryCode":            await self.service.ref_citizenship_code_nok(d),
                "refContactTypeCode":        "02",
                "contactInfo":               utils.get_str(d["NOK_MOBILE_PHONE"]),
            }

            m = {
                "rn":                               utils.get_str(d["ACCOUNT_NO"]),
                "mrn":                              utils.get_str(d["PRN"]),
                "eventDate":                        f"{d['REGISTRATION_DATE']} {d['REGISTRATION_TIME']}:00",
                "isPoliceCase":                     "00",
                "internalReferral":                 "false",
                "refReferralSourceCode":            await self.service.ref_referral_source_code(d),
                "refGenderCode":                    await self.service.ref_gender_code(d),
                "dob":                              str(d["DOB"]),
                "refMaritalStatusCode":             await self.service.ref_marital_status_code(d),
                "refReligionCode":                  await self.service.ref_religion_code(d),
                "refCitizenshipCode":               await self.service.ref_citizenship_code(d),
                "refEthnicCode":                    await self.service.ref_ethnic_code(d),
                "height":                           utils.get_num(str(d["HEIGHT"])),
                "weight":                           utils.get_num(str(d["WEIGHT"])),
                "refForeignerOriginCountryCode":    await self.service.ref_foreigner_origin_country_code(d),
                "refForeignerResidenceCountryCode": await self.service.ref_foreigner_residence_country_code(d),
                "refPersonCategoryCode":            await self.service.ref_person_category_code(d),
                "refRelationshipCode":              await self.service.ref_relationship_code(d),
                "totalDurationDay":                 "0",
                "admissionDate":                    f"{d['ADMISSION_DATE']} {d['ADMISSION_TIME']}:00",
                "person":                           person,
                "nextOfKins":                       nok,
            }

            forms.append(m)

        facilityCode = settings.FACILITYCODE
        filename = f"{facilityCode}_{ds1}_{ds2}_RH101.json"

        x = {
            "filename":           filename,
            "admissionFrom":      datefrom,
            "admissionTo":        dateto,
            "refServiceTypeCode": "02",
            "facilityCode":       facilityCode,
            "forms":              forms,
        }
        res = JsonResponse(x, json_dumps_params={'indent': 4, 'sort_keys': False})
        res.headers["Content-Disposition"] = f"attachment; filename={filename}"
        res.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        res.headers["Pragma"] = "no-cache"
        res.headers["Expires"] = "0"
        res.headers["filename"] = filename
        res.headers["Content-Type"] = "application/json"
        return res
        
    @http_get("/export/rpt1")
    async def jsonpd101(self, datefrom: str = "2023-01-01", dateto: str = "2024-01-01"):
        username = self.context.request.auth.username
        col = self.get_collection(client, username, "0")
        cur = col.find({})
        ls = utils.process_doc(list(cur))
        
        dt1 = datefrom.split("-")
        dt2 = dateto.split("-")
        ds1 = f"{dt1[2]}{dt1[1]}{dt1[0]}"
        ds2 = f"{dt2[2]}{dt2[1]}{dt2[0]}"
        
        forms = []
        for d in ls:
            person = {
                "refPersonTitleCode":        await self.service.ref_person_title_code(d),
                "fullName":                  utils.get_str(d["PATIENT_NAME"]),
                "refIdentificationTypeCode": await self.service.ref_identification_type_code(d),
                "identificationNo":          utils.get_str(d["DOCUMENT_NUMBER"]),
                "refAddressTypeCode":        "C",
                "street1":                   utils.get_str(d["STREET1"]),
                "street2":                   utils.get_str(d["STREET2"]),
                "refCityCode":               await self.service.ref_city_code(d),
                "refPostCode":               utils.get_str(d["POSTCODE"]),
                "refStateCode":              await self.service.ref_state_code(d),
                "refCountryCode":            await self.service.ref_citizenship_code(d),
                "refContactTypeCode":        "02",
                "contactInfo":               utils.get_str(d["HOME_PHONE"]),
            }
            
            nok = {
                "refPersonTitleCode":        await self.service.ref_person_title_code_nok(d),
                "fullName":                  utils.get_str(d["PATIENT_NOK_NAME"]),
                "refIdentificationTypeCode": await self.service.ref_identification_type_code_nok(d),
                "identificationNo":          utils.get_str(d["NOK_ID"]),
                "refAddressTypeCode":        "C",
                "street1":                   str(d["NOK_STREET1"]),
                "street2":                   utils.get_str(d["NOK_STREET2"]),
                "refCityCode":               await self.service.ref_city_code_nok(d),
                "refPostCode":               utils.get_str(d["NOK_POSTCODE"]),
                "refStateCode":              await self.service.ref_state_code_nok(d),
                "refCountryCode":            await self.service.ref_citizenship_code_nok(d),
                "refContactTypeCode":        "02",
                "contactInfo":               utils.get_str(d["NOK_MOBILE_PHONE"]),
            }
            
            m = {
                "rn":                               utils.get_str(d["ACCOUNT_NO"]),
                "mrn":                              utils.get_str(d["PRN"]),
                "eventDate":                        f"{d['REGISTRATION_DATE']} {d['REGISTRATION_TIME']}:00",
                "isPoliceCase":                     "02",
                "internalReferral":                 "false",
                "refReferralSourceCode":            await self.service.ref_referral_source_code(d),
                "refGenderCode":                    await self.service.ref_gender_code(d),
                "dob":                              str(d["DOB"]),
                "refMaritalStatusCode":             await self.service.ref_marital_status_code(d),
                "refReligionCode":                  await self.service.ref_religion_code(d),
                "refCitizenshipCode":               await self.service.ref_citizenship_code(d),
                "refEthnicCode":                    await self.service.ref_ethnic_code(d),
                "height":                           utils.get_num(str(d["HEIGHT"])),
                "weight":                           utils.get_num(str(d["WEIGHT"])),
                "refForeignerOriginCountryCode":    await self.service.ref_foreigner_origin_country_code(d),
                "refForeignerResidenceCountryCode": await self.service.ref_foreigner_residence_country_code(d),
                "refPersonCategoryCode":            await self.service.ref_person_category_code(d),
                "refRelationshipCode":              await self.service.ref_relationship_code(d),
                "totalDurationDay":                 "0",
                "refWardTransitionTypeCode":        "A",
                "wardDateTime":                     f"{d['ADMISSION_DATE']} {d['ADMISSION_TIME']}:00",
                "wardCode":                         utils.get_str(d["WARD_NO"]),
                "refDisciplineCode":                await self.service.ref_discipline_code(d),
                "refSpecialityCode":                await self.service.ref_discipline_code(d),
                "refSubSpecialityCode":             await self.service.ref_discipline_code(d),
                "refWardClassCode":                 await self.service.ref_ward_class_code(d),
                "refWardCategoryCode":              "00",
                "person":                           person,
                "nextOfKins":                       nok,
            }
            
            forms.append(m)
            
        facilityCode = settings.FACILITYCODE
        filename = f"{facilityCode}_{ds1}_{ds2}_PD101.json"
        
        x = {
            "filename":           filename,
            "admissionFrom":      datefrom,
            "admissionTo":        dateto,
            "refServiceTypeCode": "01",
            "facilityCode":       facilityCode,
            "forms":              forms,
        }
        res = JsonResponse(x, json_dumps_params={'indent': 4, 'sort_keys': False})
        res.headers["Content-Disposition"] = f"attachment; filename={filename}"
        res.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        res.headers["Pragma"] = "no-cache"
        res.headers["Expires"] = "0"
        res.headers["filename"] = filename
        res.headers["Content-Type"] = "application/json"
        return res
    
    @http_get("/export/rpt1/xlsx")
    async def xlsx(self, vt: str = "0", datefrom: str = "2023-01-01", dateto: str = "2024-01-01"):
        username = self.context.request.auth.username
        col = self.get_collection(client, username, vt)
        cur = col.find({})
        ls = utils.process_doc(list(cur))
        
        dt1 = datefrom.split("-")
        dt2 = dateto.split("-")
        ds1 = f"{dt1[2]}{dt1[1]}{dt1[0]}"
        ds2 = f"{dt2[2]}{dt2[1]}{dt2[0]}"
        pf = "PD101" if vt == "0" else "RH101"
        
        facilityCode = settings.FACILITYCODE
        filename = f"{facilityCode}_{ds1}_{ds2}_{pf}.xlsx"
        bx = utils.get_xlsx(COLUMN_MAP, ls)
        
        res = HttpResponse(bx.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        res.headers["Content-Disposition"] = f"attachment; filename={filename}"
        res.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        res.headers["Pragma"] = "no-cache"
        res.headers["Expires"] = "0"
        res.headers["filename"] = filename
        return res
        
    @http_get("/rpt1")
    async def list(self,
                   page: int = Query('1', alias='_page'),
                   limit: int = Query('20', alias='_limit'),
                   vt: str = "0",
                   datefrom: str = "",
                   dateto: str = ""):
        username = self.context.request.auth.username
        db = self.get_db(client, vt)
        col = db[f"__{username}__"]
        col2 = db[f"__{username}-q__"]
        total = col.count_documents({})
        
        dateFrom = datefrom
        dateTo = dateto
        t2 = col2.count_documents({})
        
        if t2 > 0:
            ld = list(col2.find({}))
            dateFrom = f"{ld[0].get('datefrom', '')}"
            dateTo = f"{ld[0].get('dateto', '')}"
            
        pg = Pager(total, int(page), int(limit))
        cur = col.find({}).skip(pg.lower_bound).limit(pg.page_size)
        ls = utils.process_doc(list(cur))
        
        for d in ls:
            d["_id"] = str(d.get("_id"))
            
        return {
            "columnmaps":  COLUMN_MAP,
            "total_count": total,
            "total_page":  pg.total_pages,
            "page":        pg.page_num,
            "data":        ls,
            "datefrom":    dateFrom,
            "dateto":      dateTo
        }
        
    @http_get("/rpt1/{id}")
    async def edit(self, id: str, vt: str = Query('0')):
        username = self.context.request.auth.username
        col = self.get_collection(client, username, vt)
        cur = col.find({"_id": ObjectId(id)})
        ls = utils.process_doc(list(cur))
        
        if len(ls) > 0:
            d = ls[0]
            d["_id"] = str(d.get("_id"))
            return d
        
        return JsonResponse({"message": "Record not found"}, status=404)
    
    @http_put("/rpt1/{id}")
    async def update(self, id: str, data: dict = Body(...), vt: str = Query('0')):
        username = self.context.request.auth.username
        col = self.get_collection(client, username, vt)
        data["_id"] = ObjectId(id)
        col.find_one_and_update({"_id": ObjectId(id)}, {"$set": data})
        return {
            "success": 1
        }

    def get_collection(self, cli: MongoClient, username: str, vt: str):
        db = self.get_db(cli, vt)
        s = f"__{username}__"
        col = db[s]
        return col

    def get_db(self, cli: MongoClient, vt: str):
        suffix = ''
        db = None
        if settings.MONGODB_PREFIX == 'prod':
            suffix = '_prod'
        
        if vt == '0':
            s = f"master_pd101{suffix}"
            db = cli[s]
            
        else:
            s = f"master_rh101{suffix}"
            db = cli[s]
            
        return db