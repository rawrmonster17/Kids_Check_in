from pydantic import BaseModel

# Base class for Kid, includes common fields used in multiple endpoints
class KidBase(BaseModel):
    first_name: str
    last_name: str
    allergies: str
    checked_in: bool

# Model used for creating a new Kid, inherits from KidBase
class KidCreate(KidBase):
    pass  # Uses the same fields as KidBase, no additional fields for creation

# Model used for reading a Kid from the database, includes an id field
class Kid(KidBase):
    id: int  # Includes ID for referencing specific Kid entries

    class Config:
        orm_mode = True  # Enable ORM mode to allow easy integration with databases

# Base class for Parent, includes common fields used in multiple endpoints
class ParentBase(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: str

# Model used for creating a new Parent, inherits from ParentBase
class ParentCreate(ParentBase):
    pass  # Uses the same fields as ParentBase, no additional fields for creation

# Model used for reading a Parent from the database, includes an id field
class Parent(ParentBase):
    id: int  # Includes ID for referencing specific Parent entries

    class Config:
        orm_mode = True  # Enable ORM mode to allow easy integration with databases

# Model used for linking a Parent to a Kid in a many-to-many relationship
class ParentKidLink(BaseModel):
    parent_id: int
    kid_id: int

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

    class Config:
        orm_mode = True  # Enable ORM mode to allow easy integration with databases

# Model used for returning JWT token details
class Token(BaseModel):
    access_token: str
    token_type: str

# Model used for token data, primarily for internal handling of authentication
class TokenData(BaseModel):
    username: str | None = None  # Username field, optional as it can be None if token is invalid
