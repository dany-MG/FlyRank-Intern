from pydantic import BaseModel, EmailStr

class AuthSchema(BaseModel):
    usr_email: EmailStr
    usr_pass: str