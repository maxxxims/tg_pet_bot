from db import async_session
from models import Volunteer, Pet
from sqlalchemy import select, insert, update, exists
from sqlalchemy.orm import joinedload
from uuid import uuid4, UUID


async def add_volounteer(tg_id: int, nick: str) -> UUID:
    user_uuid = uuid4()
    async with async_session() as session:
        async with session.begin():
            await session.execute(insert(Volunteer).values(tg_id=tg_id,
                                                        user_uuid=user_uuid, nick=nick))
            


async def is_volounteer(tg_id: int) -> bool:
    async with async_session() as session:
        async with session.begin():
            return(await session.execute(select(Volunteer.tg_id).where(Volunteer.tg_id == tg_id))).scalar() is not None

    

async def get_volunteer_pets(tg_id: int, offset: int) -> Pet:
    async with async_session() as session:   
        volunteer_first = (await session.execute(select(Volunteer).options(joinedload(
            Volunteer.pets)).where(Volunteer.tg_id == tg_id).offset(offset))).scalars().first()
        return volunteer_first.pets

async def get_volunteer(tg_id: int) -> Volunteer:
    async with async_session() as session:
        volunteer = (await session.execute(select(Volunteer).where(Volunteer.tg_id == tg_id))).scalars().first()
    return volunteer


async def get_volunteer_city(tg_id: int) -> str:
    async with async_session() as session:
        async with session.begin():
            volunteer_city = await session.execute(select(Volunteer.city).where(Volunteer.tg_id == tg_id))
    return volunteer_city.one().city


async def update_name(tg_id: int, name: str):
    async with async_session() as session:
        async with session.begin():
            await session.execute(update(Volunteer).values(name=name).where(
                Volunteer.tg_id == tg_id
            ))


async def update_surname(tg_id: int, surname: str):
    async with async_session() as session:
        async with session.begin():
            await session.execute(update(Volunteer).values(surname=surname).where(
                Volunteer.tg_id == tg_id
            ))


async def update_phone(tg_id: int, phone: str):
    async with async_session() as session:
        async with session.begin():
            await session.execute(update(Volunteer).values(phone=phone).where(
                Volunteer.tg_id == tg_id
            ))


async def update_city(tg_id: int, city: str):
    async with async_session() as session:
        async with session.begin():
            await session.execute(update(Volunteer).values(city=city).where(
                Volunteer.tg_id == tg_id
            ))



async def finish_registration(tg_id: int):
    async with async_session() as session:
        async with session.begin():
            await session.execute(update(Volunteer).values(registration_finished=True).where(
                Volunteer.tg_id == tg_id
            ))


async def update_column(tg_id: int, **kwargs):
    async with async_session() as session:
            await session.execute(update(Volunteer).values(**kwargs).where(
                Volunteer.tg_id == tg_id
            ))
            await session.commit()