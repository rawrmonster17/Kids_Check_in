# crud.py
from sqlalchemy.sql import select, insert
from models import families, users
from db import database

async def create_family(family):
    query = insert(families).values(
        parent_first_name=family.parent_first_name,
        parent_last_name=family.parent_last_name,
        parent_phone_number=family.parent_phone_number,
        parent_email=family.parent_email,
        kid_first_name=family.kid_first_name,
        kid_last_name=family.kid_last_name,
        kid_allergies=family.kid_allergies,
        kid_checked_in=family.kid_checked_in
    )
    return await database.execute(query)

async def get_families(skip: int = 0, limit: int = 10):
    query = select([families]).offset(skip).limit(limit)
    return await database.fetch_all(query)
