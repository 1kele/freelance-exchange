from datetime import datetime
from pydantic import Field
from pydantic import BaseModel


class ReviewAddRequest(BaseModel):
    order_id: int
    author_id: int
    target_id: int
    rating: int = Field(ge=1, le=5)
    text: str | None = None

class ReviewAdd(BaseModel):
    order_id: int
    target_id: int
    rating: int = Field(ge=1, le=5)
    text: str | None = None


class Review(BaseModel):
    id: int
    order_id: int
    author_id: int
    target_id: int
    rating: float = Field(ge=1, le=5)
    text: str
    created_at: datetime

class ShowReview(BaseModel):
    text: str
    rating: float = Field(ge=1, le=5)
    created_at: datetime