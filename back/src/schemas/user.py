from pydantic import BaseModel


class UserRegisterSchema(BaseModel):
    email: str
    password: str
    nickname: str




