# main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm
from schemas import FamilyCreate, UserCreate, Token, User
from crud import create_family, get_families
from db import database, engine, metadata, create_tables  # Import create_tables
from models import users, families
from auth import authenticate_user, create_access_token, get_password_hash
from datetime import timedelta
from email_funtions import send_email
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set the token expiration time (in minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Create all tables in the database
metadata.create_all(engine)
create_tables()  # Ensure tables are created

app = FastAPI()

# Mount static files for serving HTML, CSS, JS files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Database connection setup
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Root endpoint serving the main HTML page
@app.get("/")
async def root():
    return FileResponse("static/index.html")

# Endpoint for user registration
@app.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    # Hash the user's password
    hashed_password = get_password_hash(user.password)
    user_data = {**user.dict(), "hashed_password": hashed_password}
    del user_data["password"]
    # Insert the new user into the database
    query = users.insert().values(user_data)
    user_id = await database.execute(query)
    return {**user_data, "id": user_id}

# Endpoint for user login and token generation
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # Authenticate the user
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Create an access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/family/")
async def create_family_endpoint(family: FamilyCreate):
    logging.info(f"Received data: {family}")

    # Check for duplicate kid entry
    duplicate_family = await database.fetch_one(query="SELECT * FROM families WHERE kid_first_name = :kid_first_name AND kid_last_name = :kid_last_name",
                                             values={"kid_first_name": family.kid_first_name, "kid_last_name": family.kid_last_name})
    if duplicate_family:
        raise HTTPException(status_code=400, detail="Kid with the same first and last name already exists")

    family_id = await create_family(family)
    return {**family.dict(), "id": family_id}

@app.get("/families/")
async def get_families():
    query = families.select()
    return await database.fetch_all(query)

@app.put("/families/{family_id}")
async def update_family_status(family_id: int, family_update: FamilyCreate):
    query = families.update().where(families.c.id == family_id).values(kid_checked_in=family_update.kid_checked_in)
    await database.execute(query)
    return {"message": "Family status updated"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
