from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from db import database
from sqlalchemy import select
from models import users
from schemas import User, UserCreate, Token, TokenData
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Secret key and algorithm used to create and verify JWT tokens
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 password flow
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Verify if the provided password matches the hashed password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Hash the password
def get_password_hash(password):
    return pwd_context.hash(password)

# Get a user from the database by username
async def get_user(username: str):
    query = select([users]).where(users.c.username == username)
    user = await database.fetch_one(query)
    if user:
        return User(**user)
    logging.info(f"User {username} not found in the database")
    return None

# Authenticate the user by verifying the username and password
async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        logging.info(f"Authentication failed: User {username} not found")
        return False
    if not verify_password(password, user.hashed_password):
        logging.info(f"Authentication failed: Incorrect password for user {username}")
        return False
    logging.info(f"User {username} authenticated successfully")
    return user

# Create a JWT token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Get the current user from the JWT token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# Get the current active user (here we can add additional checks if needed, e.g., is_active)
async def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user
