from pydantic import BaseModel

class Kid(BaseModel):
    first_name: str
    last_name: str
    allergies: str
    checked_in: bool

class Parent(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: str

class ParentKidLink(BaseModel):
    parent_id: int
    kid_id: int
