from ninja import Field, Schema
from datetime import datetime


class LoginDto(Schema):
    username: str = Field('admin', min_length=1)
    password: str = Field('', min_length=1)
    
class User(Schema):
    password: str | None = None
    id: int = None
    username: str = ""
    first_name: str = ""
    last_name: str | None = None
    last_login: str | None = None
    
class CommonSetup(Schema):
    id: int = None
    code: str | None = ""
    created_by: int | None = None
    created_date: str | datetime | None = None
    deleted: bool | None = False
    deleted_by: int | None = None
    deleted_date: str | datetime | None = None
    desc: str | None = ""
    modified_by: int | None= None
    modified_date: str | datetime | None = None
    ref: str | None = ""