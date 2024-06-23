# db.py
import os
from sqlalchemy import create_engine, MetaData
from databases import Database
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Connect to the specified database
database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(DATABASE_URL)

# Create tables
def create_tables():
    import models  # Import models after metadata has been defined
    metadata.create_all(engine)

# Create the tables
create_tables()
