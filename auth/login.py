from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from .schema import Refresh, UserResponse, ImmResponse, TokenResponse
from .services import authenticate_user, create_access_token, get_current_admin_user, create_refresh_token, \
    verify_token, get_user, user_refresh_token_update
from database.database import get_db
from models.user import User
from auth.services import fetch_user_from_redis

auth_route = APIRouter()


@auth_route.post("/token", summary='Access Token uchun login qiling')
async def login_for_access_token(
        db: AsyncSession = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
) -> Union[TokenResponse, ImmResponse]:
    """
    Login qilish uchun yuborasiz:
     * username: **string**
     * password: **string**

   Yuborishingiz shart emas:
    * grant_type: **string**
    * scope: **string**
    * client_id: **string**
    * client_secret: **string**

    """
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login yoki parol xato!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_redis = fetch_user_from_redis(form_data.username, user)
    access_token = await create_access_token(data={"sub": user_redis["gmail"]})
    refresh_token = await create_refresh_token(data={"sub": user_redis["gmail"]})

    # Userga refresh_token yozip qoyamiz
    await user_refresh_token_update(db, user_redis["gmail"], refresh_token)
    return {
        "user": user,
        "role": user_redis["role"],
        "token_type": "bearer",
        "access_token": access_token,
        "refresh_token": refresh_token
    }


@auth_route.post("/refresh_token", summary='Refresh token orqali access token olish')
async def refresh_access_token(
        refresh: Refresh,
        db: AsyncSession = Depends(get_db)
) -> Union[TokenResponse, ImmResponse]:
    try:
        decode_token = await verify_token(refresh.token)
        username: str = decode_token.get('sub')
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token yaroqsiz!")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token yaroqsiz!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await get_user(db, username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token yaroqsiz!")

    if user.refresh_token != refresh.token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token yaroqsiz!")

    access_token = await create_access_token(data={"sub": user.gmail})
    refresh_token = await create_refresh_token(data={"sub": user.gmail})

    # Userga refresh_token yozip qoyamiz
    await user_refresh_token_update(db, user.gmail, refresh_token)

    return {
        "user": user,
        "role": user.role,
        "token_type": "bearer",
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@auth_route.get("/me", summary='O`zingiz haqingizda to`liq ma`lumot')
async def read_current_user(
        current_user: User = Depends(get_current_admin_user),
        db: AsyncSession = Depends(get_db)
) -> Union[UserResponse, ImmResponse]:
    """
    Login qilib kirganingizda o'zingiz haqingizdagi ma'umotlaringizni shu yerdan olishingiz mumkun
    """
    return current_user
