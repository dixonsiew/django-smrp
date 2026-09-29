from ninja import Field, Schema


class LoginDto(Schema):
    username: str = Field('admin', min_length=1)
    password: str = Field('', min_length=1)

class KeywordDto(Schema):
    keyword: str = ""
    
class UserDto(Schema):
    username: str = Field(..., min_length=1, max_length=150)
    password: str = Field(..., min_length=1, max_length=150)
    first_name: str = Field(..., min_length=1, max_length=150)
    last_name: str = Field(..., max_length=150)
    role_id: int = Field(..., ge=1)