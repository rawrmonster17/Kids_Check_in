from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm
from schemas import KidCreate, Kid, ParentCreate, UserCreate, Token, User
from crud import create_kid, create_parent, link_parent_kid, get_kids, get_parents
from db import database, engine, metadata
from models import users
from auth import authenticate_user, create_access_token, get_current_active_user, get_password_hash
from datetime import timedelta
from email_funtions import send_email
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set the token expiration time (in minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Create all tables in the database
metadata.create_all(engine)

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

@app.post("/add_kid_with_parent/")
async def add_kid_with_parent(request: Request):
    kid_with_parent = await request.json()
    logging.info(f"Received data: {kid_with_parent}")

    required_fields = ["kid_first_name", "kid_last_name", "kid_allergies",
                       "parent_first_name", "parent_last_name", "parent_phone_number", "parent_email"]
    for field in required_fields:
        if field not in kid_with_parent or not kid_with_parent[field]:
            raise HTTPException(status_code=400, detail=f"Missing field: {field}")

    # Check for duplicate kid entry
    duplicate_kid = await database.fetch_one(query="SELECT * FROM kids WHERE first_name = :first_name AND last_name = :last_name",
                                             values={"first_name": kid_with_parent["kid_first_name"], "last_name": kid_with_parent["kid_last_name"]})
    if duplicate_kid:
        raise HTTPException(status_code=400, detail="Kid with the same first and last name already exists")

    parent_data = {
        "first_name": kid_with_parent["parent_first_name"],
        "last_name": kid_with_parent["parent_last_name"],
        "phone_number": kid_with_parent["parent_phone_number"],
        "email": kid_with_parent["parent_email"]
    }
    parent_id = await create_parent(ParentCreate(**parent_data))

    kid_data = {
        "first_name": kid_with_parent["kid_first_name"],
        "last_name": kid_with_parent["kid_last_name"],
        "allergies": kid_with_parent["kid_allergies"],
        "checked_in": True  # Automatically set to checked in
    }
    kid_id = await create_kid(KidCreate(**kid_data))

    await link_parent_kid(parent_id, kid_id)

    return {"kid_id": kid_id, "parent_id": parent_id}


# Endpoint to create a new kid (No authentication required)
@app.post("/kids/", response_model=Kid)
async def create_kid_endpoint(kid: KidCreate):
    # Check for duplicate kid entry
    duplicate_kid = await database.fetch_one(query="SELECT * FROM kids WHERE first_name = :first_name AND last_name = :last_name",
                                             values={"first_name": kid.first_name, "last_name": kid.last_name})
    if duplicate_kid:
        raise HTTPException(status_code=400, detail="Kid with the same first and last name already exists")

    last_record_id = await create_kid(kid)
    return {**kid.dict(), "id": last_record_id}

# Endpoint to get a list of kids with pagination (No authentication required)
@app.get("/kids/", response_model=list[Kid])
async def read_kids(skip: int = 0, limit: int = 10):
    return await get_kids(skip, limit)

# Endpoint to update a kid's checked-in status (No authentication required)
@app.put("/kids/{kid_id}", response_model=Kid)
async def update_kid_endpoint(kid_id: int, kid: KidCreate):
    existing_kid = await database.fetch_one(query="SELECT * FROM kids WHERE id = :id", values={"id": kid_id})
    if not existing_kid:
        raise HTTPException(status_code=404, detail="Kid not found")
    await database.execute(query="UPDATE kids SET first_name = :first_name, last_name = :last_name, allergies = :allergies, checked_in = :checked_in WHERE id = :id",
                           values={**kid.dict(), "id": kid_id})
    return {**kid.dict(), "id": kid_id}

# Endpoint to contact a parent (Authentication required)
@app.post("/contact_parent/{kid_id}")
async def contact_parent(kid_id: int, background_tasks: BackgroundTasks, current_user: User = Depends(get_current_active_user)):
    kid = await database.fetch_one(query="SELECT * FROM kids WHERE id = :id", values={"id": kid_id})
    if not kid:
        raise HTTPException(status_code=404, detail="Kid not found")

    parent = await database.fetch_one(query="SELECT * FROM parents WHERE id = (SELECT parent_id FROM parent_kid WHERE kid_id = :kid_id)", values={"kid_id": kid_id})
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")

    email_body = f"Please attend to your child {kid['first_name']} {kid['last_name']}."

    # Send email in the background
    background_tasks.add_task(send_email, parent['email'], "Your child needs attention", email_body)

    return {"message": "Parent contacted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
