from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from db import Base
from uuid import uuid4, UUID
from datetime import datetime


class Admin(Base):
    __tablename__ = "admins"
    admin_uuid: Mapped[UUID] = mapped_column(primary_key=True)
    admin_tg_id: Mapped[int] = mapped_column(nullable=False)
    admin_nick: Mapped[str] = mapped_column(nullable=False)
    admin_username: Mapped[str] = mapped_column(nullable=False)

    channel_name: Mapped[str] = mapped_column(nullable=True)
    city: Mapped[str] = mapped_column(nullable=True)

    registration_finished: Mapped[bool] = mapped_column(default=False, nullable=False)
    show_notifications: Mapped[bool] = mapped_column(default=True, nullable=False)