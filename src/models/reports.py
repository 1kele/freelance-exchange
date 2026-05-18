import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class ReportsOrm(Base):
    __tablename__ = 'reports'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    status: Mapped[str]  # pending/ready

    file_path: Mapped[str]
    date_from: Mapped[datetime.date]
    date_to: Mapped[datetime.date]
    created_at: Mapped[datetime.date] = mapped_column(server_default=func.now())