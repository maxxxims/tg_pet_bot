from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from db import Base
from uuid import uuid4, UUID
from datetime import datetime


class Pet2Volunteer(Base):
    __tablename__ = "pet2admin"
    id: Mapped[int] = mapped_column(primary_key=True)
    pet_uuid: Mapped[UUID] = mapped_column(ForeignKey('pets.uuid', ondelete='cascade')) #, unique=False, nullable=False
    admin_tg_id: Mapped[int] = mapped_column(ForeignKey('admins.admin_tg_id', ondelete='cascade')) #mapped_column(nullable=False)
    reposted: Mapped[bool] = mapped_column(default=False, nullable=False)