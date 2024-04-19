from pathlib import Path
from database import administration_table
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)


async def register_administration_from_txt(path_to_txt: Path):
    if isinstance(path_to_txt, str):    
        path_to_txt = Path(path_to_txt)
    if not path_to_txt.exists():
        logging.info('FILE NOT FOUND')
        return
    try:
        administration_list = np.loadtxt(path_to_txt, dtype=int, ndmin=1)
        current_admin_list = await administration_table.get_administration()
        current_admin_tg_id_list = [admin.tg_id for admin in current_admin_list]
        cnt = 0
        for admin_tg_id in administration_list:
            if admin_tg_id not in current_admin_tg_id_list:
                cnt +=1
                await administration_table.add_admininistration(int(admin_tg_id))
        logging.info(f'ADDED {cnt} / {len(administration_list)} ADMINISTRATIONS')
        logging.info(f'ALL ADMINISTRATIONS: {len(current_admin_tg_id_list) + cnt}')
    except Exception as e:
        print(e)