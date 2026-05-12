import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase

_raw_db_url = os.getenv('DATABASE_URL', '')
DATABASE_URL = _raw_db_url if '+aiomysql' in _raw_db_url else _raw_db_url.replace('mysql://', 'mysql+aiomysql://')

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def connect_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('MySQL connected')

async def disconnect_db():
    await engine.dispose()
