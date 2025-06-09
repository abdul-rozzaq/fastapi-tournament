from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=5)


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=5)


class AuthResponse(BaseModel):
    user: UserRead
    token: str
