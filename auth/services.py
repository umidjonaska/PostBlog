from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta

from core.config import config
from database.database import get_db
from models.user import User
from schemas.user import UserRole
from core.redis_cli import RedisCLI

import redis
import orjson

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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


def serialize_user(user: User) -> dict:
    return {
        "id": user.id,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active,
    }


async def get_user(db: AsyncSession, email: str):
    redis_cli = RedisCLI()
    
    cached_user = redis_cli.get(email)
    if cached_user:
        return orjson.loads(cached_user)

    result = await db.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()
    if not user:
        return None

    redis_cli.set(email, serialize_user(user), expire=3600)
    return serialize_user(user)

async def authenticate_user(db: AsyncSession, username: str, password: str):
    result = await db.execute(
        select(User).where(User.username == username)
    )
    user = result.scalar_one_or_none()
    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

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
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials!",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = await verify_token(token)
    username: str = payload.get("sub")
    if not username:
        raise credentials_exception

    redis_cli = RedisCLI()
    user = redis_cli.get(username)
    if user:
        user = orjson.loads(user)
    else:
        user = await get_user(db, username)
        if not user:
            raise credentials_exception

    return user

async def get_current_admin_user(current_user: dict = Depends(get_current_user)):
    if UserRole(current_user["role"]) != UserRole.ADMIN:
        raise HTTPException(status_code=406, detail="Ruxsat yo‘q")
    return current_user


async def user_refresh_token_update(db: AsyncSession, email: str, token: str):
    '''
    Refresh tokendi update qilamiz
    '''
    if token:
        stmt = (
            update(User)
            .where(User.email == email)
            .values(refresh_token=token)
        )
        await db.execute(stmt)
        await db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Ma'lumot bo'sh")
    return True