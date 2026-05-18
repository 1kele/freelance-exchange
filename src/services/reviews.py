from src.exceptions import PermissionDeniedException, ReviewCommentRequiredException, \
    OrderNotCompletedException, SelfReviewForbiddenException, ReviewAlreadyExistsException, \
    InvalidReviewParticipantsException, UserNotFoundException, ObjectNotFoundException
from src.schemas.order import OrderStatus
from src.schemas.review import ReviewAdd, ReviewAddRequest, ShowReview
from src.schemas.user import UserAVGRating
from src.services.base import BaseService


class ReviewService(BaseService):


    async def create_review(
            self,
            data: ReviewAdd,
            user_id: int
    ) -> None:
        order_id = data.order_id
        full_info = await self.db.order.get_one(id=order_id)
        if user_id != full_info.customer_id and user_id != full_info.freelancer_id:
            raise PermissionDeniedException

        if full_info.freelancer_id != data.target_id and full_info.customer_id != data.target_id:
            raise InvalidReviewParticipantsException

        if not data.text and data.rating < 5:
            raise ReviewCommentRequiredException

        if full_info.status != OrderStatus.completed:
            raise OrderNotCompletedException

        if data.target_id == user_id:
            raise SelfReviewForbiddenException

        existing = await self.db.review.get_filter_by(order_id=data.order_id, author_id=user_id)
        if existing:
            raise ReviewAlreadyExistsException

        reviews = await self.db.review.get_filter_by(target_id=data.target_id)
        count = len(reviews) + 1
        current_user_data = await self.db.user.get_one(id=data.target_id)
        new_rating = round((current_user_data.rating * (count - 1) + data.rating) / count, 2)
        new_data = ReviewAddRequest(author_id=user_id, **data.model_dump())
        await self.db.review.add(new_data)
        await self.db.user.edit(UserAVGRating(rating=new_rating),id=data.target_id)
        await self.db.commit()


    async def get_all_reviews(
            self,
            user_id: int
    ) -> list[ShowReview]:
        try:
            await self.db.user.get_one(id=user_id)
        except ObjectNotFoundException:
            raise UserNotFoundException
        reviews = await self.db.review.get_filter_by(target_id=user_id)
        formated_reviews = [ShowReview.model_validate(r, from_attributes=True) for r in reviews]
        return formated_reviews