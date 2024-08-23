from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True


class UserCreate(UserBase):
    email: EmailStr
    password: str
    is_active: bool = True


class UserUpdate(UserBase):
    pass


class User(UserBase):
    id: int
