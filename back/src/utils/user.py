from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import User

from sqlalchemy import select

import random


async def get_user_by_email(session: AsyncSession, email: str):
    stmt = select(User).where(User.email == email)

    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if user is not None:
        return user
    else:
        return None


async def get_user_by_tag(session: AsyncSession, tag: str):
    stmt = select(User).where(User.tag == tag)

    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if user is not None:
        return user
    else:
        return None


async def add_user(session: AsyncSession, **kwargs) -> User:
    user_data = kwargs
    user_data["email_code"] = int(''.join(random.choices('0123456789', k=6)))

    while True:
        user_tag = ''.join(random.choices('0123456789', k=8))
        user_using_tag = await get_user_by_tag(session, user_tag)
        if user_using_tag is None:
            break  # Найден уникальный тег, выходим из цикла

    user_data["tag"] = user_tag

    print(user_data)
    new_user = User(**user_data)
    session.add(new_user)
    await session.commit()
    return new_user


