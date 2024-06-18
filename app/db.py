import os
import psycopg2
from sqlalchemy import create_engine, MetaData
from databases import Database
from dotenv import load_dotenv
from urllib.parse import urlparse

# Load environment variables from a .env file
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Parse the DATABASE_URL to extract components
parsed_url = urlparse(DATABASE_URL)
db_name = parsed_url.path[1:]  # Remove the leading '/'
db_user = parsed_url.username
db_pass = parsed_url.password
db_host = parsed_url.hostname
db_port = parsed_url.port

# Connection URL without the database name, for initial connection
initial_db_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/postgres"

def create_database_if_not_exists():
    # Connect to the default 'postgres' database to check if our target database exists
    conn = psycopg2.connect(initial_db_url)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'")
    exists = cur.fetchone()
    if not exists:
        cur.execute(f"CREATE DATABASE {db_name}")
    cur.close()
    conn.close()

# Ensure the database exists
create_database_if_not_exists()

# Connect to the specified database
database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(DATABASE_URL)
