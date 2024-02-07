from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from config import load_db_url
import asyncio


engine = create_async_engine(load_db_url(), echo=False)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    ...



async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main():
    from models import Pet
    from uuid import UUID
    from sqlalchemy import select, insert, update
    await init_db()
    async with async_session() as session:
        async with session.begin():
            pet = (await session.execute(select(Pet).where(Pet.uuid == UUID('a76c9f4ba0414414a4e47038b0ba7cfa')))).one()
            # for el in pet:
    print(pet.uuid)
    # for p in pet:
    #     print(p.uuid)

    # print(f'pet = {pet}')
    # t = pet.one()
    # print(pet.__dict__, type(pet.one()))
            
        #     print(t['uuid'])
    # for t in pet:
    #     print(t[0].uuid)

if __name__ == "__main__":
    asyncio.run(main())