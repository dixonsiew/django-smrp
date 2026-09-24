from ninja import Field, Schema


class LoginDto(Schema):
    username: str = Field('admin', min_length=1)
    password: str = Field('', min_length=1)