from fastapi import APIRouter, Depends, HTTPException, Form, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette import status

from src.db import get_session
from src.schemas.user import UserRegisterSchema, UserMainInfo, CardCreateSchema, CardMainInfo, BoughtCardMainInfo, \
    CreateDeckSchema, BoughtCardCreateSchema, AddCardsToDeckRequestSchema
# from src.utils import get_user, create_user, increment_clicks
# from src.utils.users import add_password, get_user_for_password, put_is_banned
# from datetime import datetime, timedelta
from src.utils.card import add_card, get_card_by_name, get_all_cards, get_card_by_id, buy_card, get_all_cards_in_shop, \
    add_card_to_shop, add_deck, get_bought_cards, get_user_decks, get_all_bought_cards, add_card_to_deck, \
    get_cards_from_deck, remove_cards_from_deck

from src.utils.security import get_password_hash, authenticate_user, create_access_token, get_current_user
from src.utils.user import add_user, get_user_by_email, get_me, update_is_auntificate

cards_router = APIRouter()


@cards_router.post("/add", response_model=CardCreateSchema)
async def add_card_api(
        card: CardCreateSchema,
        current_user: dict = Depends(get_current_user)
):
    """Добавляем карту"""

    if current_user.access.name != 'admin':
        raise HTTPException(status_code=403, detail="У вас нет доступа к этому ресурсу")

    card = {
        "name": card.name,
        "lore_description": card.lore_description,
        "image_url": card.image_url,
        "price_shop": card.price_shop,
        "price_mana": card.price_mana,
        "attack": card.attack,
        "defense": card.defense,
        "rarity": card.rarity,
        "classOfCard": card.classOfCard,
    }

    existing_card = await get_card_by_name(current_user.session, card["name"])

    if existing_card:
        raise HTTPException(status_code=409, detail="Карта с таким именем уже существует")

    cardAdd = await add_card(current_user.session, **card)
    try:
        await current_user.session.commit()
        if cardAdd:
            return cardAdd
    except Exception as e:
        await current_user.session.rollback()
        return e


@cards_router.get("/all-cards", response_model=list[CardMainInfo])
async def get_all_cards_api(
        current_user: dict = Depends(get_current_user),
        limit: int = Query(default=20, ge=1, le=100),
        offset: int = Query(default=0, ge=0),
        shop: bool = Query(default=False)
):
    """Выводим все карты в игре"""

    offset = offset * limit

    if shop:
        cards = await get_all_cards_in_shop(current_user.session, limit, offset)
    else:
        cards = await get_all_cards(current_user.session, limit, offset)

    if not cards:
        raise HTTPException(status_code=404, detail="Карты не найдены")
    return cards


@cards_router.post("/buy")
async def buy_card_api(
        bought_card: BoughtCardCreateSchema,
        current_user: dict = Depends(get_current_user)
):
    """Покупаем карту"""

    bought_card = {
        "card_in_shop_id": bought_card.card_in_shop_id
    }

    card = await get_card_by_id(current_user.session, bought_card['card_in_shop_id'])
    user = await get_me(current_user.session, current_user.id)

    if not card:
        raise HTTPException(status_code=404, detail="Такой карты не существует")

    if not card.is_for_sale:
        raise HTTPException(status_code=403, detail="Карта не продается")

    if current_user.gem < card.price_shop:
        raise HTTPException(status_code=402, detail="Недостаточно средств для покупки")

    new_bought = await buy_card(current_user.session, user, card)

    if new_bought:
        return new_bought
    else:
        return {f"Карта успешно куплена"}


@cards_router.put("/add-to-shop")
async def add_card_to_shop_api(
        card_id: int,
        current_user: dict = Depends(get_current_user)
):
    """Добавляем карту в магазин"""

    if current_user.access.name != 'admin':
        raise HTTPException(status_code=403, detail="У вас нет доступа к этому ресурсу")

    card = await get_card_by_id(session=current_user.session, id=card_id)

    if not card:
        raise HTTPException(status_code=404, detail="Такой карты не существует")

    if card.is_for_sale:
        raise HTTPException(status_code=403, detail="Карта уже в магазине")

    new_card_status_in_shop = await add_card_to_shop(current_user.session, card)

    if new_card_status_in_shop:
        return {f'Карта теперь продается'}


@cards_router.get("/bought-cards", response_model=list[BoughtCardMainInfo])
async def get_bought_cards_api(
        current_user: dict = Depends(get_current_user),
        limit: int = Query(default=20, ge=1, le=100),
        offset: int = Query(default=0, ge=0),
):
    """Получаем купленные пользователем карты"""
    offset = offset * limit

    bought_cards = await get_bought_cards(session=current_user.session, user_id=current_user.id, limit=limit,
                                          offset=offset)

    if not bought_cards:
        raise HTTPException(status_code=404, detail="Карт не найдено")

    return bought_cards


@cards_router.post("/add-deck")
async def add_deck_api(
        deck: CreateDeckSchema,
        current_user: dict = Depends(get_current_user)
):
    """Добавляем колоду"""

    deck = {
        "name": deck.name
    }

    if len(deck['name']) < 6 or len(deck['name']) > 30:
        raise HTTPException(status_code=491, detail="Название колоды должно быть больше 6 символов и меньше 30")

    new_deck = await add_deck(session=current_user.session, user_id=current_user.id, **deck)

    if new_deck:
        return {f"Колода {deck['name']} успешно добавлена"}


@cards_router.get("/decks")
async def get_decks_api(
        current_user: dict = Depends(get_current_user),
        limit: int = Query(default=20, ge=1, le=100),
        offset: int = Query(default=0, ge=0),
):
    """Получаем колоды пользователя"""

    offset = offset * limit

    user_decks = await get_user_decks(session=current_user.session, user_id=current_user.id, limit=limit,
                                      offset=offset)

    if not user_decks:
        raise HTTPException(status_code=404, detail="Колоды не найдены")

    return user_decks


@cards_router.post("/add-card-to-deck")
async def add_cards_to_deck_api(
        request_data: AddCardsToDeckRequestSchema,
        current_user: dict = Depends(get_current_user),
):
    """Добавляем карты в колоду"""

    cards_in_deck_request = await get_cards_from_deck(current_user.session, current_user.id, request_data.deck_id)
    cards_in_deck = [item.bought_card.id for item in cards_in_deck_request]

    added_cards = []

    # Получаем все купленные карты текущего пользователя
    bought_cards = await get_all_bought_cards(current_user.session, current_user.id)

    # Создаем множество ID купленных карт
    bought_cards_ids = [item.id for item in bought_cards]

    count = 0

    # Проверяем каждую карту из запроса на наличие ее ID в купленных картах пользователя
    for card_id in request_data.card_ids:
        if card_id not in bought_cards_ids:
            raise HTTPException(status_code=403, detail=f"Карта с ID {card_id} не куплена пользователем")

        if card_id in cards_in_deck:
            raise HTTPException(status_code=403, detail=f"Карта с ID {card_id} уже есть в колоде")

        added_cards.append({
            "user_deck_id": request_data.deck_id,
            "bought_card_id": card_id
        })
        count += 1
    new_added_card_to_deck = await add_card_to_deck(current_user.session, added_cards)
    if new_added_card_to_deck:
        return {f'Добавлено {count} карт'}


@cards_router.delete("/remove-card-from-deck")
async def remove_card_from_deck_api(
        request_data: AddCardsToDeckRequestSchema,
        current_user: dict = Depends(get_current_user)
):
    """Удаляем карты из колоды"""

    cards_in_deck_request = await get_cards_from_deck(current_user.session, current_user.id, request_data.deck_id)
    cards_in_deck = [item.bought_card.id for item in cards_in_deck_request]

    removed_cards = []

    # Получаем все купленные карты текущего пользователя
    bought_cards = await get_all_bought_cards(current_user.session, current_user.id)

    # Создаем множество ID купленных карт
    bought_cards_ids = [item.id for item in bought_cards]

    count = 0

    # Проверяем каждую карту из запроса на наличие ее ID в купленных картах пользователя
    for card_id in request_data.card_ids:
        if card_id not in bought_cards_ids:
            raise HTTPException(status_code=403, detail=f"Карта с ID {card_id} не куплена пользователем")

        if card_id not in cards_in_deck:
            raise HTTPException(status_code=403, detail=f"Карта с ID {card_id} не в колоде")

        removed_cards.append({
            "user_deck_id": request_data.deck_id,
            "bought_card_id": card_id
        })
        count += 1
    new_removed_cards_from_deck = await remove_cards_from_deck(current_user.session, removed_cards)
    if new_removed_cards_from_deck:
        return {f'Удалено {count} карт'}


