# schemas.py
from pydantic import BaseModel, EmailStr

# Schema for creating a Family
class FamilyCreate(BaseModel):
    parent_first_name: str
    parent_last_name: str
    parent_phone_number: str
    parent_email: EmailStr
    kid_first_name: str
    kid_last_name: str
    kid_allergies: str
    kid_checked_in: bool


# Model used for reading a Family from the database, includes an id field
class Family(FamilyCreate):
    id: int

    class Config:
        orm_mode = True  # Enable ORM mode to allow easy integration with databases

# Base class for User, includes common fields used in authentication
class UserBase(BaseModel):
    username: str
    email: str

# Model used for creating a new User, includes password field for account setup
class UserCreate(UserBase):
    password: str  # Password field needed for user registration

# Model used for reading a User from the database, includes an id field
class User(UserBase):
    id: int  # Includes ID for referencing specific User entries
    hashed_password: str  # Hashed password for secure storage

    class Config:
        orm_mode = True  # Enable ORM mode to allow easy integration with databases

# Model used for returning JWT token details
class Token(BaseModel):
    access_token: str
    token_type: str

# Model used for token data, primarily for internal handling of authentication
class TokenData(BaseModel):
    username: str | None = None  # Username field, optional as it can be None if token is invalid

class SMSRequest(BaseModel):
    to: str
    message: str
