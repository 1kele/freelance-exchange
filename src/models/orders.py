import datetime
from decimal import Decimal

from sqlalchemy import func, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class OrdersOrm(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    category: Mapped[str]
    deadline_days: Mapped[int]
    deadline_date: Mapped[datetime.date | None] = mapped_column(
        nullable=True, default=None
    )
    status: Mapped[str] = mapped_column(default="free")

    customer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    freelancer_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True, default=None
    )
    created_at: Mapped[datetime.date] = mapped_column(server_default=func.now())
    is_overdue: Mapped[bool] = mapped_column(default=False)
