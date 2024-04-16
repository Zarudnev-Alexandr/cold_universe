from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

# from src import users_router
# from src.routers.shop import shop_router
from src.routers.user import users_router

app = FastAPI(debug=True)

origins = ["http://localhost", "http://localhost:8080", "http://localhost:3000", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def start():
    print("Поехали")


app.include_router(users_router, prefix="/api/users", tags=["Users"])
# app.include_router(shop_router, prefix="/api/shop", tags=["Shop"])



# bot.include_router(src.users_router, prefix="/api/users", tags=["Users"])
#
# bot.include_router(src.chats_router, prefix="/api/chats", tags=["Chats"])
#
# bot.include_router(src.messages_router, prefix="/api/messages", tags=["Messages"])
#
# bot.include_router(src.bootcamps_router, prefix="/api/bootcamps", tags=["Bootcamps"])
#
# bot.include_router(src.websocket_router, prefix="/api/ws", tags=["WS_Messages"])