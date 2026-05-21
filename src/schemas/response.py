from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel


class ResponseStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"


class ResponseAddRequest(BaseModel):
    order_id: int
    freelancer_id: int
    cover_letter: str
    proposed_price: Decimal
    status: ResponseStatus = ResponseStatus.pending


class ResponseAdd(BaseModel):
    cover_letter: str
    proposed_price: Decimal


class Response(BaseModel):
    id: int
    order_id: int
    freelancer_id: int
    cover_letter: str
    proposed_price: Decimal
    status: ResponseStatus
    created_at: datetime


class ResponseStatusRequest(BaseModel):
    status: ResponseStatus
