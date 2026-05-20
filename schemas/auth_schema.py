from pydantic import BaseModel, EmailStr, field_validator

class LoginSchema(BaseModel):
    email: str
    password: str

class RegisterSchema(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v