from db import async_session
from models import Pet, Volunteer
from sqlalchemy import select, insert, update, delete, and_, desc
from uuid import uuid4, UUID
from sqlalchemy.orm import joinedload


async def add_new_pet(volunteer_tg_id: int) -> UUID:
    uuid = uuid4()
    async with async_session() as session:
        async with session.begin():
            await session.execute(insert(Pet).values(volunteer_tg_id=volunteer_tg_id, uuid=uuid))
    return uuid


# async def get_info_from_pet(uuid: UUID) -> Pet:
#     async with async_session() as session:
#         async with session.begin():
#             pet = (await session.execute(select(Pet).where(Pet.uuid == uuid))).one()
#     return pet


async def get_info_from_pet(uuid: UUID) -> Pet:
    """async with async_session() as session:
        async with session.begin():
            # pet = (await session.execute(select(Pet.pet_photo_id, Pet.volunteer_tg_id, Pet.volunteer_nick,
            #                                     Pet.description,
            #                                     Pet.pet_type
            #                                     ).where(Pet.uuid == uuid))).one()

            pet = (await session.execute(select(Pet).options(
                joinedload(Pet.volunteer)).where(Pet.uuid == uuid))).scalars().one()
    return pet"""
    async with async_session() as session:
        pet = await session.scalar(select(Pet).options(joinedload(Pet.volunteer)).where(Pet.uuid == uuid))
    return pet


async def get_available_pet(pet_type: str, offset: int) -> Pet:
    """async with async_session() as session:
        async with session.begin():
            pets = (await session.execute(select(Pet.uuid, Pet.description,
                                                      Pet.pet_photo_id, Pet.volunteer_nick, Pet.volunteer_tg_id
                                                      ).where(Pet.pet_type == pet_type,
                                                              Pet.available == True).offset(offset))).first()
    return pets"""
    async with async_session() as session:
        # pets = (await session.execute(select(Pet).options(joinedload(Pet.volunteer)).where(
        #     Pet.pet_type == pet_type, Pet.available == True).offset(offset))).first()   
        pets = (await session.execute(select(Pet).options(joinedload(
            Pet.volunteer)).where(Pet.pet_type == pet_type, Pet.available == True).offset(offset))).scalars().first()
        return pets
    

async def get_available_pet_in_city(city: str, offset: int) -> Pet:
    async with async_session() as session:
        pets = (await session.execute(select(Pet).options(joinedload(
            Pet.volunteer)).where(Pet.city == city,
            Pet.available == True).order_by(Pet.created_time.desc()).offset(offset))).scalars().first()
        return pets
    


async def delete_pet_card(uuid: UUID) -> Pet:
    async with async_session() as session:
        async with session.begin():
            await session.execute(delete(Pet).where(Pet.uuid == uuid))
            await session.commit()
        



async def get_volinteer_pets(tg_id: int, offset: int, owner: bool = False) -> Pet:
    async with async_session() as session:
        if owner:
            pets = (await session.execute(select(Pet).options(joinedload(
                Pet.volunteer)).where(Volunteer.tg_id == tg_id, Pet.available == True
                                      ).order_by(Pet.created_time.desc()).offset(offset))).scalars().first()
            # PROD VERSION #
        else:
            pets = (await session.execute(select(Pet).options(joinedload(
                Pet.volunteer)).where(
                    and_(Pet.volunteer_tg_id == tg_id, Pet.available == True)
                    ).order_by(Pet.created_time.desc()).offset(offset))).scalars().first()
        return pets


async def get_prompt(uuid: UUID) -> str:
    async with async_session() as session:
        async with session.begin():
            prompt = await session.execute(select(Pet.prompt).where(Pet.uuid == uuid))
    print(f'prompt = {prompt}')
    return prompt.one().prompt


async def get_description(uuid: UUID) -> str:
    async with async_session() as session:
        async with session.begin():
            description = await session.execute(select(Pet.description).where(Pet.uuid == uuid))
    # print(f'description = {description}')
    return description.one().description


async def update_pet_column(uuid: UUID, **kwargs):
    async with async_session() as session:
            await session.execute(update(Pet).values(**kwargs).where(
                Pet.uuid == uuid
            ))
            await session.commit()


async def get_pet_type(uuid: UUID) -> str:
    async with async_session() as session:
        async with session.begin():
            pet_type = await session.execute(select(Pet.pet_type).where(Pet.uuid == uuid))
    return pet_type.one().pet_type


async def update_pet_gender(gender: str, uuid: UUID):
    async with async_session() as session:
            await session.execute(update(Pet).values(gender=gender).where(
                Pet.uuid == uuid
            ))


async def update_pet_type(pet_type: str, uuid: UUID):
    async with async_session() as session:
        async with session.begin():
            await session.execute(update(Pet).values(pet_type=pet_type).where(
                Pet.uuid == uuid
            ))


async def delete_pet(uuid: UUID):
    async with async_session() as session:
        async with session.begin():
            await session.execute(delete(Pet).where(
                Pet.uuid == uuid
            ))


async def update_pet_prompt(prompt: str, uuid: UUID):
    async with async_session() as session:
        async with session.begin():
            await session.execute(update(Pet).values(prompt=prompt).where(
                Pet.uuid == uuid
            ))


async def update_pet_description(description: str, uuid: UUID):
    async with async_session() as session:
        async with session.begin():
            await session.execute(update(Pet).values(description=description).where(
                Pet.uuid == uuid
            ))


async def update_pet_photo(pet_photo_id: str, uuid: UUID):
    async with async_session() as session:
        async with session.begin():
            await session.execute(update(Pet).values(pet_photo_id=pet_photo_id).where(
                Pet.uuid == uuid
            ))


async def update_available_pet(available: bool, uuid: UUID):
    async with async_session() as session:
        async with session.begin():
            await session.execute(update(Pet).values(available=available).where(
                Pet.uuid == uuid
            ))