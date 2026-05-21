from datetime import datetime, date
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict


class OrderStatus(str, Enum):
    free = "free"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"


class OrderCategory(str, Enum):
    design = "design"
    development = "development"
    marketing = "marketing"
    copywriting = "copywriting"
    testing = "testing"
    devops = "devops"
    data_science = "data_science"
    mobile = "mobile"
    seo = "seo"
    video = "video"
    photo = "photo"
    translation = "translation"
    other = "other"


class OrderAdd(BaseModel):
    title: str
    description: str
    price: Decimal
    category: OrderCategory
    deadline_days: int
    customer_id: int


class OrderAddRequest(BaseModel):
    title: str
    description: str
    price: Decimal
    category: OrderCategory
    deadline_days: int


class Order(BaseModel):
    id: int
    title: str
    description: str
    price: Decimal
    category: str
    deadline_days: int
    deadline_date: datetime
    status: OrderCategory
    customer_id: int
    freelancer_id: int
    created_at: datetime
    is_overdue: bool

    model_config = ConfigDict(from_attributes=True)


class OrderPatch(BaseModel):
    title: str | None = None
    description: str | None = None
    price: Decimal | None = None
    category: OrderCategory | None = None
    deadline_days: int | None = None


class OrderPatchStatus(BaseModel):
    status: OrderStatus
    is_overdue: bool


class OrderCancel(BaseModel):
    status: OrderStatus


class OrderAccept(BaseModel):
    freelancer_id: int
    status: OrderStatus
    deadline_date: date
