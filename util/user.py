import os
import psycopg2
from psycopg2 import sql
from passlib.context import CryptContext

# Environment variables for database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/kids")

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to get password hash
def get_password_hash(password):
    return pwd_context.hash(password)

# User details
username = "chris"
email = "beck.chris88@outlook.com"
password = "test"

# Connect to the database
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Hash the password
hashed_password = get_password_hash(password)

# Insert the user into the database
insert_query = sql.SQL("""
    INSERT INTO users (username, email, hashed_password) 
    VALUES (%s, %s, %s)
""")
cur.execute(insert_query, (username, email, hashed_password))

# Commit the transaction and close the connection
conn.commit()
cur.close()
conn.close()

print("User created successfully.")
