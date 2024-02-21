from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from db import Base
from uuid import uuid4, UUID
from datetime import datetime


class Pet(Base):
    __tablename__ = "pets"
    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    volunteer_tg_id: Mapped[int] = mapped_column(ForeignKey('volunteers.tg_id'))
    # volunteer_nick: Mapped[int] = mapped_column(ForeignKey('volunteers.nick'))

    pet_type: Mapped[str] = mapped_column(default=None, nullable=True)

    gender: Mapped[str] = mapped_column(default=None, nullable=True)
    name: Mapped[str] = mapped_column(default=None, nullable=True)

    age: Mapped[str] = mapped_column(default=None, nullable=True)
    weight: Mapped[int] = mapped_column(default=None, nullable=True)

    has_chip: Mapped[bool] = mapped_column(default=None, nullable=True)
    vaccinations: Mapped[str] = mapped_column(default=None, nullable=True)
    castration: Mapped[bool] = mapped_column(default=None, nullable=True)
    special_care: Mapped[str] = mapped_column(default=None, nullable=True)

    prompt: Mapped[str] = mapped_column(default=None, nullable=True)
    description: Mapped[str] = mapped_column(default=None, nullable=True)
    pet_photo_id: Mapped[str] = mapped_column(default=None, nullable=True)

    city: Mapped[str] = mapped_column(default=None, nullable=True)

    created_time: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    available: Mapped[bool] = mapped_column(default=False)

    volunteer: Mapped["Volunteer"] = relationship()#= relationship("Volunteer", back_populates="pets")
