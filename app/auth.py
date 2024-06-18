from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy import select
from db import database
from models import users
from schemas import TokenData, User

# Define OAuth2 password bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Define the password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key to encode/decode JWT tokens
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

# Function to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to hash password
def get_password_hash(password):
    return pwd_context.hash(password)

# Function to authenticate user
async def authenticate_user(username: str, password: str):
    query = select([users]).where(users.c.username == username)
    user = await database.fetch_one(query)
    if user is None:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Function to create JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to get current user from token
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
    except (JWTError, ValidationError):
        raise credentials_exception
    query = select([users]).where(users.c.username == token_data.username)
    user = await database.fetch_one(query)
    if user is None:
        raise credentials_exception
    return user

# Function to get current active user
async def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user
