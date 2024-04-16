import os
import sys

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

current_dir = os.path.dirname(__file__)

config_reader_dir = os.path.abspath(os.path.join(current_dir, "../../"))
print(config_reader_dir)

sys.path.append(config_reader_dir)

from config_reader import config

engine = create_async_engine(url=str(config.db_url), echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session