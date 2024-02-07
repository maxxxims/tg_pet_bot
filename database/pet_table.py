from db import async_session
from models import Pet
from sqlalchemy import select, insert, update
from uuid import uuid4, UUID


async def add_new_pet(owner_id: int, owner_nick: str) -> UUID:
    uuid = uuid4()
    async with async_session() as session:
        async with session.begin():
            await session.execute(insert(Pet).values(owner_id=owner_id, uuid=uuid, owner_nick=owner_nick))
    return uuid


async def get_info_from_pet(uuid: UUID) -> Pet:
    async with async_session() as session:
        async with session.begin():
            pet = (await session.execute(select(Pet).where(Pet.uuid == uuid))).one()
    return pet


async def get_info_from_pet(uuid: UUID) -> Pet:
    async with async_session() as session:
        async with session.begin():
            pet = (await session.execute(select(Pet.pet_photo_id,
                                                Pet.description,
                                                Pet.pet_type
                                                ).where(Pet.uuid == uuid))).one()
    return pet


async def get_available_pet(pet_type: str, offset: int) -> Pet:
    async with async_session() as session:
        async with session.begin():
            pets = (await session.execute(select(Pet.uuid, Pet.description,
                                                      Pet.pet_photo_id, Pet.owner_nick, Pet.owner_id
                                                      ).where(Pet.pet_type == pet_type,
                                                              Pet.available == True).offset(offset))).first()
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
    print(f'description = {description}')
    return description.one().description


async def update_pet_type(pet_type: str, uuid: UUID):
    async with async_session() as session:
        async with session.begin():
            await session.execute(update(Pet).values(pet_type=pet_type).where(
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