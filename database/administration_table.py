from db import async_session
from models import Administration
from sqlalchemy import select, insert, update, exists, delete
from sqlalchemy.orm import joinedload
from uuid import uuid4, UUID


async def add_admininistration(admin_tg_id: int) -> UUID:
    admin_uuid = uuid4()
    async with async_session() as session:
        async with session.begin():
            await session.execute(insert(Administration).values(tg_id=admin_tg_id, uuid=admin_uuid))
    return admin_uuid


async def get_administration():
    async with async_session() as session:   
        admins = (await session.execute(select(Administration))).scalars()
    if admins is None:
        return []
    return admins


async def get_administration_ids():
    async with async_session() as session:   
        admins = (await session.execute(select(Administration))).scalars()
    if admins is None:
        return []
    return [admin.tg_id for admin in admins]


async def update_search_city(tg_id: int, city: str):
    async with async_session() as session:
        async with session.begin():
            await session.execute(update(Administration).values(city_to_search=city).where(Administration.tg_id == tg_id))
            

async def get_search_city(tg_id: int) -> str:
    async with async_session() as session:
        city = (await session.execute(select(Administration.city_to_search).where(Administration.tg_id == tg_id))).scalars().first()
    return city


async def update_current_offset(tg_id: int, offset: str):
    async with async_session() as session:
        async with session.begin():
            await session.execute(update(Administration).values(current_offset=offset).where(Administration.tg_id == tg_id))
            

async def get_current_offset(tg_id: int):
    async with async_session() as session:
        offset = (await session.execute(select(Administration.current_offset).where(Administration.tg_id == tg_id))).scalars().first()
    print(f'OFFSET = {offset}')
    return offset