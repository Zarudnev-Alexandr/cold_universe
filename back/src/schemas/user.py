from typing import List

from pydantic import BaseModel, EmailStr, constr
import datetime


class UserRegisterSchema(BaseModel):
    """Схема данных для регистрации пользователя."""

    email: EmailStr
    password: str
    nickname: str


class AccessInfo(BaseModel):
    # access_id: int
    name: str


class CardCreateSchema(BaseModel):
    name: str
    lore_description: str
    image_url: str
    price_shop: int
    price_mana: int
    attack: int
    defense: int
    rarity: int
    classOfCard: str


class CardMainInfo(CardCreateSchema):
    id: int


class BoughtCardMainInfo(BaseModel):
    id: int
    level: int
    card: CardMainInfo


class BoughtCardCreateSchema(BaseModel):
    card_in_shop_id: int


class UserMainInfo(BaseModel):
    """Схема данных пользователя для главного меню"""

    email: str
    nickname: str
    is_confirmed_email: bool
    tag: str
    level: int
    exp: int
    gem: int
    date_of_create: datetime.datetime
    access: AccessInfo


class CreateDeckSchema(BaseModel):
    name: str


class AddCardsToDeckRequestSchema(BaseModel):
    deck_id: int
    card_ids: List[int]
