from pydantic import BaseModel, EmailStr, constr
import datetime


class UserRegisterSchema(BaseModel):
    """Схема данных для регистрации пользователя."""

    email: EmailStr
    password: str
    nickname: str


class UserMainInfo(BaseModel):
    """Схема данных пользователя для главного меню"""

    email: str
    nickname: str
    is_confirmed_email: bool
    tag: str
    level: int
    exp: int
    gold: int
    gem: int
    date_of_create: datetime.datetime
