from models import Pet2Volunteer
from db import async_session
from models import Volunteer, Pet, Admin
from sqlalchemy import select, insert, update, exists, and_, text
from sqlalchemy.orm import joinedload
from uuid import uuid4, UUID
import pandas as pd


async def register_sent_msg(admin_tg_id: int, pet_uuid: UUID, reposted: bool = False):
    async with async_session() as session:
        async with session.begin():
            await session.execute(insert(Pet2Volunteer).values(
                admin_tg_id=admin_tg_id, pet_uuid=pet_uuid, reposted=reposted))


async def repost_card(admin_tg_id: int, pet_uuid: UUID):
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                update(Pet2Volunteer).where(and_(
                Pet2Volunteer.admin_tg_id == admin_tg_id,
                Pet2Volunteer.pet_uuid == pet_uuid
            )).values(reposted=True)
            )

async def has_reposted(admin_tg_id: int, pet_uuid: UUID) -> Pet2Volunteer:
    async with async_session() as session:
        async with session.begin():
            has_raw = (await session.execute(
                select(Pet2Volunteer.reposted).where(and_(
                    Pet2Volunteer.admin_tg_id == admin_tg_id,
                    Pet2Volunteer.pet_uuid == pet_uuid
                ))
            )).scalars().first()#is not None
    return has_raw

async def get_admin_pets(admin_city: str, offset: int, admin_tg_id: int) -> Pet:
    print(f'START')
    async with async_session() as session:
        async with session.begin():
            print(f'IN SESSION')
            res = await session.execute(
                text(f"""SELECT * FROM (SELECT * FROM pets WHERE city = '{admin_city}' and available = true)
                        LEFT JOIN pet2admin 
                                ON uuid = pet2admin.pet_uuid
                                    LEFT JOIN volunteers 
                                        ON volunteers.tg_id = volunteer_tg_id
                        WHERE pet2admin.reposted is NULL or pet2admin.reposted = false and pet2admin.admin_tg_id = {admin_tg_id}
                        ORDER BY created_time DESC
                        LIMIT 1 OFFSET {offset} """))
    print(f'AFTER!')     
    for el in res:
        # v = Volunteer(tg_id=el.tg_id, name=el.nick, username=el.username)
        # el.__setattr__('volunteer', v)
        # print('INSERT VOLUNTEER!')
        return el
    return None