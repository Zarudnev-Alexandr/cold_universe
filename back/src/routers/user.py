from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.db import get_session
from src.schemas.user import UserRegisterSchema, UserMainInfo

from src.utils.security import get_password_hash, authenticate_user, create_access_token, get_current_user
from src.utils.user import add_user, get_user_by_email, get_me, update_is_auntificate

users_router = APIRouter()


@users_router.post("/register")
async def add_user_api(user: UserRegisterSchema, session: AsyncSession = Depends(get_session)):
    """
    ### Регистрация нового пользователя

    Регистрирует нового пользователя в системе.

    #### Параметры:

    - **email (str)**: Провалидирован до знака @, короче, если будет написана всякая муть, но с собакой, то по идее
    пропустит, хотя, я хз, там валидация из библиотеки.
    - **password (str)**: Длина пароля: **(6 < pass < 40)**
    - **nickname (str)**: Длина ника: **(6 < pass < 30)**

    #### Возвращаемое значение:

    При регистрации вернутся все данные о пользователе

    #### Исключения:

    - **409 Conflict**: Если пользователь с таким email уже существует.
    - **Остальные**: Все кроме 409 писал не я, так что просто внимательнее в ответ смотри)
    """

    if len(user.password) < 6 or len(user.password) > 40:
        raise HTTPException(status_code=491, detail="Пароль должен быть больше 6 символов и меньше 40")

    elif len(user.nickname) < 6 or len(user.nickname) > 30:
        raise HTTPException(status_code=492, detail="Никнейм должен быть больше 6 символов и меньше 30")

    user_data = {
        "email": user.email,
        "password": get_password_hash(user.password),
        "nickname": user.nickname,
    }

    user_by_email = await get_user_by_email(session, user.email)

    if user_by_email:
        raise HTTPException(status_code=409, detail="Пользователь с таким email уже существует")

    user_add = await add_user(session, **user_data)

    if user_add:
        return {f"Пользователь {user.nickname} успешно зарегистрирован"}


@users_router.post("/login")
async def login_api(
        email: str = Form(...),
        password: str = Form(...),
        session: AsyncSession = Depends(get_session),
):
    """### Логин пользователя

    получаем токен после логина

    #### Параметры:

    - **email (str)**
    - **password (str)**:

    #### Возвращаемое значение:

     - **access_token (str)**
     - **token_type (str)**: По дефолту bearer
    """

    user = await authenticate_user(session, email, password)
    if user:
        access_token = await create_access_token(data={"email": user.email})
        return JSONResponse(
            content={
                "access_token": access_token,
                "token_type": "bearer",
                # "user_id": str(user.id),
            },
            status_code=status.HTTP_200_OK,
        )
    else:
        return JSONResponse(
            content={"message": "Неверный email или пароль"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


@users_router.get("/me", response_model=UserMainInfo)
async def get_me_api(current_user: dict = Depends(get_current_user)):
    """
    ### Основная инфа о пользователе

    В главное меню вкинуть этого будет достаточно

    #### Параметры:

    - **token (str)**: Не налажать с токеном и все нормас будет

    #### Возвращаемое значение:

    Там снизу схема есть

    #### Исключения:

    - **401 Unauthorized**: Если с токеном напортачить
    """
    print(current_user.__dict__)
    return (
        current_user
        if current_user
        else JSONResponse(
            content={"message": "Такого пользователя не существует"}, status_code=404
        )
    )


@users_router.put("/confirm_mail", response_model=UserMainInfo)
async def put_confirmed_email_api(email_code: int = Form(...),
                                  current_user: dict = Depends(get_current_user)):
    """
       ### Подтверждение почты

       Если код неправильный или уже почта подтвержденная, то пошлет

       #### Параметры:

       - **token (str)**: дефолт токен
       - **email_code (int)**: сам код подтверждения, всегда 6 цифр

       #### Возвращаемое значение:

       Основаная схема пользователя

       #### Исключения:

       - **409 Unauthorized**: Почта уже подтверждена
       - **400 Bad Request**: Неправильный код подтверждения
       """
    user = await get_me(current_user.session, current_user.id)

    if user.is_confirmed_email:
        raise HTTPException(status_code=409, detail="Почта уже подтверждена")

    if user.email_code != email_code:
        raise HTTPException(status_code=400, detail="Неправильный код подтверждения")

    updated_is_authenticate_confirmed = await update_is_auntificate(current_user.session, user)

    return updated_is_authenticate_confirmed
