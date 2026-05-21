import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class ResponsesOrm(Base):
    __tablename__ = "responds"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    freelancer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    cover_letter: Mapped[str]
    proposed_price: Mapped[float]
    status: Mapped[str]  # pending/accepted/rejected
    created_at: Mapped[datetime.date] = mapped_column(server_default=func.now())
