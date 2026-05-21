from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, ConfigDict


class PublicRole(str, Enum):
    customer = "customer"
    freelancer = "freelancer"


class AllRoles(str, Enum):
    customer = "customer"
    freelancer = "freelancer"
    admin = "admin"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserAddRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

    first_name: str
    last_name: str
    middle_name: str

    role: PublicRole


class UserAdd(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str

    first_name: str
    last_name: str
    middle_name: str

    role: PublicRole


class User(BaseModel):
    id: int
    email: EmailStr
    username: str
    hashed_password: str
    first_name: str
    last_name: str
    middle_name: str
    role: PublicRole
    is_blocked: bool
    rating: float
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    middle_name: str
    role: AllRoles
    rating: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserPatch(BaseModel):
    username: str | None = None
    email: EmailStr | None = None

    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None

    role: PublicRole | None = None


class PublicUserInformation(BaseModel):
    id: int
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    middle_name: str
    rating: float
    role: AllRoles
    created_at: datetime


class AdminUserUpdate(BaseModel):
    role: AllRoles


class UserAVGRating(BaseModel):
    rating: float


class UserForAdmin(BaseModel):
    id: int
    email: str
    username: str
    first_name: str
    last_name: str
    middle_name: str
    role: str
    is_blocked: bool
    rating: float
    created_at: datetime


class UserBlock(BaseModel):
    is_blocked: bool
