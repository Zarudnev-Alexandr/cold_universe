import os

from pydantic_settings import BaseSettings
from pydantic import PostgresDsn

from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    db_url: PostgresDsn = os.getenv("db_url")

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()
