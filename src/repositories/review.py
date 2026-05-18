from src.models.reviews import ReviewsOrm
from src.repositories.base import BaseRepositories
from src.schemas.review import Review


class ReviewRepository(BaseRepositories):
    model = ReviewsOrm
    schema = Review