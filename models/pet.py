from sqlalchemy.orm import Mapped, mapped_column
from db import Base
from uuid import uuid4, UUID
from datetime import datetime

class Pet(Base):
    __tablename__ = "animals"
    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(nullable=False)
    owner_nick: Mapped[str] = mapped_column(nullable=False)
    pet_type: Mapped[str] = mapped_column(default=None, nullable=True)
    prompt: Mapped[str] = mapped_column(default=None, nullable=True)
    description: Mapped[str] = mapped_column(default=None, nullable=True)
    pet_photo_id: Mapped[str] = mapped_column(default=None, nullable=True)

    created_time: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    available: Mapped[bool] = mapped_column(default=False)

