from sqlalchemy import Table, Column, Integer, String, Text, Boolean, ForeignKey
from db import metadata

kids = Table(
    "kids",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("first_name", String(50)),
    Column("last_name", String(50)),
    Column("allergies", Text),
    Column("checked_in", Boolean)
)

parents = Table(
    "parents",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("first_name", String(50)),
    Column("last_name", String(50)),
    Column("phone_number", String(20)),
    Column("email", String(100))
)

parent_kid = Table(
    "parent_kid",
    metadata,
    Column("parent_id", Integer, ForeignKey("parents.id")),
    Column("kid_id", Integer, ForeignKey("kids.id")),
    primary_key=True
)
