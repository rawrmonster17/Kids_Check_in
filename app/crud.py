from sqlalchemy.sql import select, insert
from models import kids, parents, parent_kid
from db import database

async def create_kid(kid):
    query = insert(kids).values(
        first_name=kid.first_name,
        last_name=kid.last_name,
        allergies=kid.allergies,
        checked_in=kid.checked_in
    )
    return await database.execute(query)

async def create_parent(parent):
    query = insert(parents).values(
        first_name=parent.first_name,
        last_name=parent.last_name,
        phone_number=parent.phone_number,
        email=parent.email
    )
    return await database.execute(query)

async def link_parent_kid(parent_id, kid_id):
    query = insert(parent_kid).values(
        parent_id=parent_id,
        kid_id=kid_id
    )
    return await database.execute(query)

async def get_kids(skip: int = 0, limit: int = 10):
    query = select([kids]).offset(skip).limit(limit)
    return await database.fetch_all(query)

async def get_parents(skip: int = 0, limit: int = 10):
    query = select([parents]).offset(skip).limit(limit)
    return await database.fetch_all(query)

async def get_parent_kids(parent_id: int):
    query = select([kids]).select_from(
        kids.join(parent_kid, kids.c.id == parent_kid.c.kid_id)
    ).where(parent_kid.c.parent_id == parent_id)
    return await database.fetch_all(query)
