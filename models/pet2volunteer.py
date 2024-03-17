from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from db import Base
from uuid import uuid4, UUID
from datetime import datetime


class Pet2Volunteer(Base):
    __tablename__ = "pet2admin"
    id: Mapped[int] = mapped_column(primary_key=True)
    pet_uuid: Mapped[UUID] = mapped_column(ForeignKey('pets.uuid', ondelete='CASCADE',
                                                       onupdate="CASCADE"))
    admin_tg_id: Mapped[int] = mapped_column(ForeignKey('admins.admin_tg_id',
                                                         ondelete='CASCADE', onupdate="CASCADE"))
    reposted: Mapped[bool] = mapped_column(default=False, nullable=False)
    #pet: Mapped["Pet"] = relationship(cascade='all, delete', passive_deletes=True)
    #admin: Mapped["Admin"] = relationship(cascade='all, delete', passive_deletes=True)