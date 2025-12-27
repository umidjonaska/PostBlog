from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta

from core.config import config
from database.database import get_db
from models.user import User
from schemas.user import UserRole
from core.redis_cli import RedisCLI

import redis
import orjson

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def fetch_user_from_redis(key, value):
    r = redis.Redis(host='localhost', port=6379, db=0)
    user_data = r.get(key)  # Fetch from Redis
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        # Try to decode the data as JSON
        if isinstance(user_data, (bytes, str)):
            user_dict = orjson.loads(user_data)
        elif isinstance(user_data, dict):  # Directly usable
            user_dict = user_data
        else:
            raise ValueError("Unexpected data format")
    except orjson.JSONDecodeError as e:
        raise ValueError(f"Error decoding user data: {e}")

    return user_dict

async def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def verify_token(token: str):
    try:
        payload = jwt.decode(token, config.app.secret_key, algorithms=[config.app.algorithm])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token yaroqsiz!",
            headers={"WWW-Authenticate": "Bearer"},
        )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def get_user(db: AsyncSession, gmail: str):
    r = RedisCLI()
    user = r.connect_redis_and_get(hall=gmail)
    if user:
        print("Redis record found, logged by redis")
        return user
    
    result = await db.execute(select(User).filter(User.gmail == gmail))
    user = result.scalars().first()
    print("Query came from database")
    if user:
        r.set(gmail, user)
        print(f"Redis was written for {gmail}")
    return user

async def authenticate_user(db: AsyncSession, gmail: str, password: str):
    user = await get_user(db, gmail)  # Fetch user
    
    # Check if `user` is a serialized JSON or byte string
    if isinstance(user, (str, bytes)):
        # Deserialize JSON from Redis
        user = orjson.loads(user)
    
    # Check if `user` is a dictionary (from Redis)
    if isinstance(user, dict):
        password_hash = user.get("password_hash")
    else:
        password_hash = user.password_hash

    if not password_hash:
        print("No password hash found")
        return False

    # Verify the password
    verify_pw = verify_password(password, password_hash)
    if not verify_pw:
        print("Password verification failed")
        return False

    return user



async def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=config.app.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.app.secret_key, algorithm=config.app.algorithm)
    return encoded_jwt


async def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=config.app.refresh_token_expire_days)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.app.secret_key, algorithm=config.app.algorithm)
    return encoded_jwt


async def get_current_user(
        db: AsyncSession = Depends(get_db),
        token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials!",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = await verify_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        #token_data = TokenData(username=username)
        r = RedisCLI()
        user_data = r.connect_redis_and_get(username)
    except JWTError:
        raise credentials_exception
    
    user_dict = orjson.loads(user_data)
    return User(**user_dict)

    # user = await get_user(database, username=token_data.username)
    # if user is None:
    #     raise credentials_exception
    # return user


async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=406, detail="Sizda bu ma'lumotlarni olishga ruxsat yo'q")
    return current_user

async def get_current_sale_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.SOTUV and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=406, detail="Sizda bu ma'lumotlarni olishga ruxsat yo'q")
    return current_user

async def get_current_manufacture_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.ISHLAB_CHIQARISH and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=406, detail="Sizda bu ma'lumotlarni olishga ruxsat yo'q")
    return current_user


async def user_refresh_token_update(db: AsyncSession, gmail: str, token: str):
    '''
    Refresh tokendi update qilamiz
    '''
    if token:
        stmt = (
            update(User)
            .where(User.gmail == gmail)
            .values(refresh_token=token)
        )
        await db.execute(stmt)
        await db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Ma'lumot bo'sh")
    return True
