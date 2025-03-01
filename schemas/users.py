from pydantic import BaseModel, EmailStr


class UserSignupSchema(BaseModel):
    email: EmailStr
    password: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"

    model_config = {
        "from_attributes": True,
    }
