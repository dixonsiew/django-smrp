from ninja import Field, Schema


class LoginDto(Schema):
    username: str = Field('admin', min_length=1)
    password: str = Field('admin123', min_length=1)
    
class RefreshTokenDto(Schema):
    refresh_token: str = ""
    
class ChangePasswordDto(Schema):
    password: str = Field(..., min_length=1, max_length=150)
    confirm_password: str = Field(..., min_length=1, max_length=150)

class KeywordDto(Schema):
    keyword: str = ""
    
class UserDto(Schema):
    username: str = Field(..., min_length=1, max_length=150)
    password: str = Field(..., min_length=1, max_length=150)
    first_name: str = Field(..., min_length=1, max_length=150)
    last_name: str = Field(..., max_length=150)
    role_id: int = Field(..., ge=1)
    
class ReportQueryDto(Schema):
    page: int = Field(1, alias='_page', ge=1)
    limit: int = Field(20, alias='_limit', ge=1)
    vt: int = Field(...)
    datefrom: str = Field("", max_length=10)
    dateto: str = Field("", max_length=10)