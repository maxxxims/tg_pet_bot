from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base
from uuid import uuid4, UUID
from datetime import datetime


class Volunteer(Base):
    __tablename__ = "volunteers"
    user_uuid: Mapped[UUID] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(nullable=False)
    nick: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=True, default=None)

    name: Mapped[str] = mapped_column(default=None, nullable=True)
    surname: Mapped[str] = mapped_column(default=None, nullable=True)
    phone: Mapped[str] = mapped_column(default=None, nullable=True)
    city: Mapped[str] = mapped_column(default=None, nullable=True)

    registered_time: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    registration_finished: Mapped[bool] = mapped_column(default=False)

    pets: Mapped['Pet'] = relationship("Pet", back_populates="volunteer")