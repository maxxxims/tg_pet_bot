from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from db import Base
from uuid import uuid4, UUID
from datetime import datetime


class Administration(Base):
    __tablename__ = "administraion"
    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(nullable=False)
    city_to_search: Mapped[str] = mapped_column(nullable=True)
    show_notifications: Mapped[bool] = mapped_column(default=True, nullable=False)
    current_offset: Mapped[int] = mapped_column(default=0, nullable=True)