from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import User

from sqlalchemy import select

import random
import smtplib
from email.mime.text import MIMEText


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


# Функция для отправки письма с кодом регистрации
async def send_registration_code(email: str, code: str):
    sender_email = "alexandrzarudnev57@gmail.com"  # Укажите ваш email
    sender_password = "geip kvxc pctt wgkk"  # Укажите пароль от вашего email

    message = MIMEText(f"Твой код регистрации: {code} \n\n Добро пожаловать в ❄Cold Universe🔥")

    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = "Код регистрации Cold Universe"

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:  # Укажите SMTP-сервер и порт
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, [email], message.as_string())


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

    await send_registration_code(user_data["email"], str(user_data["email_code"]))

    return new_user


async def get_me(session: AsyncSession, id: int):
    user = await session.get(User, id)
    return user


async def update_is_auntificate(session, user, id):
    user.is_confirmed_email = True

    await session.commit()
    return user

