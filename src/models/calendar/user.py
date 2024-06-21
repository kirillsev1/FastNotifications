from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.meta import Base

if TYPE_CHECKING:
    from src.models.calendar.note import Note


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)

    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)

    password: Mapped[str] = mapped_column(String)

    utc: Mapped[int] = mapped_column(Integer, unique=True, default=0)

    note: Mapped['Note'] = relationship('Note', back_populates='user')
