# models.py
from sqlalchemy import Table, Column, Integer, String, Text, Boolean
from db import metadata

# Define the families table
families = Table(
    "families",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("parent_first_name", String(50)),
    Column("parent_last_name", String(50)),
    Column("parent_phone_number", String(20)),
    Column("parent_email", String(100)),
    Column("kid_first_name", String(50)),
    Column("kid_last_name", String(50)),
    Column("kid_allergies", Text),
    Column("kid_checked_in", Boolean)
)

# Define the users table
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(50), unique=True, index=True),
    Column("email", String(100), unique=True, index=True),
    Column("hashed_password", String(100))
)
