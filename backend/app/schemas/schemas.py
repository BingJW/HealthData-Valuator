from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict, AliasChoices, field_validator

class InputModel(BaseModel):
    model_config = ConfigDict(extra='forbid')

class UserLogin(InputModel):
    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1, max_length=256)

    @field_validator('username')
    @classmethod
    def clean_username(cls, value):
        value = value.strip()
        if not value:
            raise ValueError('用户名不能为空')
        return value

class UserRegister(UserLogin):
    password: str = Field(min_length=6, max_length=256)
    hospital: str = Field(min_length=1, max_length=200)
    phone: str = Field(default='', max_length=20)
    email: str = Field(default='', max_length=100)

    @field_validator('hospital')
    @classmethod
    def clean_hospital(cls, value):
        if not value.strip():
            raise ValueError('医院名称不能为空')
        return value.strip()

class AdminUserCreate(UserLogin):
    password: str = Field(min_length=6, max_length=256)
    hospital: str = Field(default='', max_length=200)
    phone: str = Field(default='', max_length=20)
    email: str = Field(default='', max_length=100)

class UserProfileUpdate(InputModel):
    hospital: Optional[str] = Field(default=None, max_length=200)
    phone: Optional[str] = Field(default=None, max_length=20)
    email: Optional[str] = Field(default=None, max_length=100)

class AdminUserUpdate(UserProfileUpdate):
    password: Optional[str] = Field(default=None, min_length=6, max_length=256)

class Indicator(InputModel):
    category: int = Field(ge=1, le=9)
    item_name: str = Field(min_length=1, max_length=200)
    amount: Decimal = Field(ge=0, le=1000000000000, max_digits=15, decimal_places=2, allow_inf_nan=False)

class EvaluationCreate(InputModel):
    name: str = Field(min_length=1, max_length=200, validation_alias=AliasChoices('name', 'evaluation_name'))
    description: str = Field(default='', max_length=500)
    indicators: list[Indicator] = Field(min_length=1, max_length=100)

    @field_validator('name')
    @classmethod
    def clean_name(cls, value):
        if not value.strip():
            raise ValueError('评估名称不能为空')
        return value.strip()

class EvaluationUpdate(InputModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=500)
    indicators: Optional[list[Indicator]] = Field(default=None, min_length=1, max_length=100)

    @field_validator('name')
    @classmethod
    def clean_name(cls, value):
        if value is not None and not value.strip():
            raise ValueError('评估名称不能为空')
        return value.strip() if value is not None else value
