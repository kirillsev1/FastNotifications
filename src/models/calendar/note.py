from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.meta import DEFAULT_SCHEMA, Base

if TYPE_CHECKING:
    from src.models.calendar.user import User


class Note(Base):
    __tablename__ = 'note'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(f'{DEFAULT_SCHEMA}.user.id'))

    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)

    perform: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    content: Mapped[str] = mapped_column(String)

    send_required: Mapped[bool] = mapped_column(Boolean)

    user: Mapped['User'] = relationship('User', back_populates='note')
