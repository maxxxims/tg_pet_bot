from db import async_session
from models import Volunteer, Pet, Admin
from sqlalchemy import select, insert, update, exists
from sqlalchemy.orm import joinedload
from uuid import uuid4, UUID
import pandas as pd



async def get_statistics():
    async with async_session() as session:   
        pet_table = (await session.execute(select(Pet).where(Pet.available == True))).scalars().all()
        volunteer_table = (await session.execute(select(Volunteer).where(Volunteer.registration_finished == True))).scalars().all()
        admin_table = (await session.execute(select(Admin).where(Admin.registration_finished == True))).scalars().all()

        pet_list, volunter_list, admin_list = [], [], []
        for pet in pet_table:
            pet_list.append(pet.__dict__)
        for volunteer in volunteer_table:
            volunter_list.append(volunteer.__dict__)
        for admin in admin_table:
            admin_list.append(admin.__dict__)

        df_pet_table = pd.DataFrame(pet_list)#, columns=['uuid', 'city', 'pet_type', 'age'])
        df_volunteer_table = pd.DataFrame(volunter_list, columns=['name', 'surname', 'nick', 'city', 'registered_time', 'tg_id'])
        df_admin_table = pd.DataFrame(admin_list, columns=['channel_name', 'admin_nick', 'city'])

        return df_pet_table, df_volunteer_table, df_admin_table
        # {
        #     'df_pet_table': df_pet_table,
        #     'df_volunteer_table': df_volunteer_table,
        #     'df_admin_table': df_admin_table
        # }