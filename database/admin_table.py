from db import async_session
from models import Volunteer, Pet, Admin
from sqlalchemy import select, insert, update, exists, delete
from sqlalchemy.orm import joinedload
from uuid import uuid4, UUID


async def add_admin(admin_tg_id: int, admin_nick: str, admin_username: str) -> UUID:
    admin_uuid = uuid4()
    async with async_session() as session:
        async with session.begin():
            await session.execute(insert(Admin).values(admin_tg_id=admin_tg_id, admin_username=admin_username,
                                                        admin_uuid=admin_uuid, admin_nick=admin_nick))
    return admin_uuid



async def update_admin_column(admin_tg_id: int, **kwargs):
    async with async_session() as session:
            async with session.begin():
                await session.execute(update(Admin).values(**kwargs).where(
                    Admin.admin_tg_id == admin_tg_id
                ))
            # await session.commit()


async def get_admins_for_notifications(city: str):
    async with async_session() as session:   
        admins = (await session.execute(select(Admin).where(Admin.city == city,
                                                            Admin.show_notifications == True))).scalars()
        return admins


async def get_admin(admin_tg_id: int) -> Admin:
    async with async_session() as session:
        return (await session.execute(select(Admin).where(Admin.admin_tg_id == admin_tg_id))).scalars().first()


async def get_admin_city(admin_tg_id: str) -> str:
    async with async_session() as session:   
        city = (await session.execute(select(Admin.city).where(Admin.admin_tg_id == admin_tg_id,
                                                            ))).scalars().first()
        return city


async def is_admin(tg_id: int) -> bool:
    async with async_session() as session:
        async with session.begin():
            return (await session.execute(
                select(Admin.admin_tg_id).where(Admin.admin_tg_id == tg_id))).scalar() is not None



async def finish_registration(admin_tg_id: int):
    async with async_session() as session:
            async with session.begin():
                await session.execute(update(Admin).values(registration_finished=True).where(
                    Admin.admin_tg_id == admin_tg_id
                ))



async def delete_admin(admin_tg_id: int):
    async with async_session() as session:
        async with session.begin():
            await session.execute(delete(Admin).where(Admin.admin_tg_id == admin_tg_id))
            await session.commit()