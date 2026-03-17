import re
from pydantic import BaseModel, EmailStr, field_validator

class UserCreate(BaseModel):
    email: EmailStr
    password: str

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        # 1. Length Check
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        
        # 2. Number Check
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one number')
        
        # 3. Letter Check
        if not any(char.isalpha() for char in v):
            raise ValueError('Password must contain at least one letter')
        
        # 4. Special Character Check
        # This looks for characters like ! @ # $ % etc.
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError('Password must contain at least one special character')
            
        return v

# This schema is what we send BACK to the user (hiding the password)
class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str

    class Config:
        from_attributes = True
        