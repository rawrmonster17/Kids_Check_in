from sqlalchemy import Table, Column, Integer, String, Text, Boolean, ForeignKey
from db import metadata

# Define the kids table
kids = Table(
    "kids",
    metadata,
    Column("id", Integer, primary_key=True),  # Primary key for the kids table
    Column("first_name", String(50)),         # First name of the kid
    Column("last_name", String(50)),          # Last name of the kid
    Column("allergies", Text),                # Allergies information for the kid
    Column("checked_in", Boolean)             # Check-in status of the kid
)

# Define the parents table
parents = Table(
    "parents",
    metadata,
    Column("id", Integer, primary_key=True),  # Primary key for the parents table
    Column("first_name", String(50)),         # First name of the parent
    Column("last_name", String(50)),          # Last name of the parent
    Column("phone_number", String(20)),       # Phone number of the parent
    Column("email", String(100))              # Email address of the parent
)

# Define the parent_kid table for the many-to-many relationship between parents and kids
parent_kid = Table(
    "parent_kid",
    metadata,
    Column("parent_id", Integer, ForeignKey("parents.id"), primary_key=True),  # Foreign key to the parents table
    Column("kid_id", Integer, ForeignKey("kids.id"), primary_key=True)         # Foreign key to the kids table
)

# Define the users table for authentication
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),                 # Primary key for the users table
    Column("username", String(50), unique=True, index=True), # Username for the user, must be unique
    Column("email", String(100), unique=True, index=True),   # Email for the user, must be unique
    Column("hashed_password", String(100))                   # Hashed password for the user
)
