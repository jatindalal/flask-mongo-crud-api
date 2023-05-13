from pydantic import BaseModel, EmailStr, root_validator
from typing import Optional

class NewUser(BaseModel):
    _id: str
    name: str
    email: EmailStr
    password: str

class UpdatedUser(BaseModel):
    _id: str
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    @root_validator
    def any_of(cls, v):
        if not any(v.values()):
            raise ValueError('one of name, email or password must have a value to be updated')
        return v