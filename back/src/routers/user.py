from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.db import get_session
from src.schemas.user import UserRegisterSchema
# from src.utils import get_user, create_user, increment_clicks
# from src.utils.users import add_password, get_user_for_password, put_is_banned
# from datetime import datetime, timedelta

from src.utils.security import get_password_hash
from src.utils.user import add_user, get_user_by_email

users_router = APIRouter()


@users_router.post("/register")
async def add_user_api(user: UserRegisterSchema, session: AsyncSession = Depends(get_session)):
    user_data = {
        "email": user.email,
        "password": get_password_hash(user.password),
        "nickname": user.nickname,
    }

    user_by_email = await get_user_by_email(session, user.email)

    if user_by_email:
        raise HTTPException(status_code=401, detail="Пользователь с таким email уже существует")

    user_add = await add_user(session, **user_data)

    if user_add:
        return user_add
