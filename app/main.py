from fastapi import FastAPI, HTTPException, Depends
from schemas import Kid, Parent, ParentKidLink
from crud import create_kid, create_parent, link_parent_kid, get_kids, get_parents, get_parent_kids
from db import database, engine, metadata

# Create all tables in the database
metadata.create_all(engine)

app = FastAPI()

# Event handler for startup - connect to the database
@app.on_event("startup")
async def startup():
    await database.connect()

# Event handler for shutdown - disconnect from the database
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Endpoint to create a new kid
@app.post("/kids/", response_model=Kid)
async def create_kid_endpoint(kid: Kid):
    last_record_id = await create_kid(kid)
    return {**kid.dict(), "id": last_record_id}

# Endpoint to create a new parent
@app.post("/parents/", response_model=Parent)
async def create_parent_endpoint(parent: Parent):
    last_record_id = await create_parent(parent)
    return {**parent.dict(), "id": last_record_id}

# Endpoint to link a parent to a kid
@app.post("/parent_kid/", response_model=ParentKidLink)
async def link_parent_kid_endpoint(link: ParentKidLink):
    await link_parent_kid(link)
    return link

# Endpoint to get a list of kids with pagination
@app.get("/kids/", response_model=list[Kid])
async def read_kids(skip: int = 0, limit: int = 10):
    return await get_kids(skip, limit)

# Endpoint to get a list of parents with pagination
@app.get("/parents/", response_model=list[Parent])
async def read_parents(skip: int = 0, limit: int = 10):
    return await get_parents(skip, limit)

# Endpoint to get a list of kids linked to a specific parent
@app.get("/parent_kids/{parent_id}", response_model=list[Kid])
async def read_parent_kids(parent_id: int):
    return await get_parent_kids(parent_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
