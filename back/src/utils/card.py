from typing import Any, Sequence, List

from fastapi import HTTPException
from sqlalchemy import select, Row, RowMapping, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import User, Access, Card, BoughtCard, UserDeck, BoughtCardInDeck

from sqlalchemy import select


async def add_card(session: AsyncSession, **kwargs) -> Card:
    new_card = Card(**kwargs)
    session.add(new_card)
    return new_card


async def get_card_by_name(session: AsyncSession, name: str):
    existing_card = await session.execute(select(Card).where(Card.name == name))
    return existing_card.scalars().first()


async def get_all_cards(session: AsyncSession, limit: int, offset: int) -> Sequence[Row[Any] | RowMapping | Any]:
    """Получаем все карты"""

    result = await session.execute(
        select(Card)
        .offset(offset)
        .limit(limit)
    )
    return result.scalars().all()


async def get_all_cards_in_shop(session: AsyncSession, limit: int, offset: int) -> Sequence[Row[Any] | RowMapping | Any]:
    """Получаем все карты в магазине"""

    result = await session.execute(
        select(Card)
        .where(Card.is_for_sale)
        .offset(offset)
        .limit(limit)
    )
    return result.scalars().all()


async def get_card_by_id(session: AsyncSession, id: int):
    """Получаем карту по id"""

    card = await session.get(Card, id)
    return card


async def buy_card(session, user, card):
    """Покупка карты"""

    new_bought = BoughtCard(user_id=user.id, card_id=card.id, level=1)
    session.add(new_bought)
    await session.commit()

    if new_bought:
        user.gem = user.gem - card.price_shop
        await session.commit()
        await session.flush()
        return new_bought


async def add_card_to_shop(session, card):
    """Помещаем карту в магазин"""

    card.is_for_sale = True

    await session.commit()
    return card.is_for_sale


async def get_bought_cards(session: AsyncSession, user_id: int, limit: int, offset: int) -> Sequence[Row[Any] |
                                                                                                 RowMapping | Any]:
    """Получаем купленные пользователем карты"""

    result = await session.execute(
        select(BoughtCard)
        .where(BoughtCard.user_id == user_id)
        .offset(offset)
        .limit(limit)
    )
    return result.scalars().all()


async def get_all_bought_cards(session: AsyncSession, user_id: int):
    """Получаем все купленные пользователем карты"""

    result = await session.execute(
        select(BoughtCard)
        .where(BoughtCard.user_id == user_id)
    )
    return result.scalars().all()


async def add_deck(session: AsyncSession, user_id: int, **kwargs):
    """Добавляем колоду"""

    user_deck_data = kwargs
    user_deck_data["user_id"] = user_id

    new_user_deck = UserDeck(**kwargs)
    session.add(new_user_deck)
    await session.commit()
    return new_user_deck


async def get_user_decks(session: AsyncSession, user_id: int, limit: int, offset: int) -> Sequence[Row[Any] |
                                                                                                 RowMapping | Any]:
    """Получаем колоды пользователя"""
    result = await session.execute(
        select(UserDeck)
        .where(UserDeck.user_id == user_id)
        .offset(offset)
        .limit(limit)
    )
    return result.unique().scalars().all()


async def add_card_to_deck(session: AsyncSession, cards: List[dict]):
    """Добавляем карты в колоду"""

    for card in cards:
        new_added_card_to_deck = BoughtCardInDeck(**card)
        session.add(new_added_card_to_deck)
        await session.commit()
    return True


async def get_cards_from_deck(session: AsyncSession, user_id: int, user_deck_id: int):
    """Получаем все карты из колоды"""

    user_deck = await session.get(UserDeck, user_deck_id)

    if user_deck is None:
        raise HTTPException(status_code=404, detail="Колода не найдена")

    if user_deck.user_id != user_id:
        raise HTTPException(status_code=403, detail="У вас нет доступа к этой колоде, она чужая")

    cards_in_deck = user_deck.bought_cards_in_deck

    return cards_in_deck


async def remove_cards_from_deck(session: AsyncSession, cards: List[dict]):
    """Кдаляем карты из колоды"""

    for card in cards:
        print(card)
        stmt = (
            delete(BoughtCardInDeck)
            .where(BoughtCardInDeck.bought_card_id == card['bought_card_id'])
            .where(BoughtCardInDeck.user_deck_id == card['user_deck_id'])
        )
        await session.execute(stmt)
        await session.commit()
    return True

