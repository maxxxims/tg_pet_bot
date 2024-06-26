from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, joinedload
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from config import load_db_url
import asyncio


db_url = load_db_url()
print(f'DB URL = {db_url}')
engine = create_async_engine(db_url, echo=False)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    ...



async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        


async def drop_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
    except Exception as e:
        print(e)

async def main():
    from models import Pet, Volunteer, Admin, Pet2Volunteer
    from uuid import UUID
    from sqlalchemy import select, insert, update, text, delete
    await init_db()

    async with async_session() as session:
        async with session.begin():
            await session.execute(delete(Pet).where(Pet.uuid == UUID('e3f429689a4f46d89243dd7a75dfcae4')))


if __name__ == "__main__":
    asyncio.run(main())