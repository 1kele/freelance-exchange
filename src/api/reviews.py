from fastapi import APIRouter

from src.api.dependencies import DBDep, CurrentUserDep
from src.exceptions import PermissionDeniedException, ReviewCommentRequiredException, \
    OrderNotCompletedException, SelfReviewForbiddenException, InvalidReviewParticipantsException, \
    ReviewAlreadyExistsException, InvalidReviewParticipantsHTTPException, ReviewCommentRequiredHTTPException, \
    PermissionDeniedHTTPException, OrderNotCompletedHTTPException, SelfReviewForbiddenHTTPException, \
    ReviewAlreadyExistsHTTPException, ObjectNotFoundHTTPException, ObjectNotFoundException, UserNotFoundException, \
    UserNotFoundHTTPException
from src.schemas.review import ReviewAdd
from src.services.reviews import ReviewService

router = APIRouter(prefix="/reviews", tags=["Отзывы"])

@router.post("")
async def add_review(
        db: DBDep,
        data: ReviewAdd,
        current_user: CurrentUserDep
):
    try:
        await ReviewService(db).create_review(data, current_user.id)
    except PermissionDeniedException:
        raise PermissionDeniedHTTPException

    except InvalidReviewParticipantsException:
        raise InvalidReviewParticipantsHTTPException

    except ReviewCommentRequiredException:
        raise ReviewCommentRequiredHTTPException

    except OrderNotCompletedException:
        raise OrderNotCompletedHTTPException

    except SelfReviewForbiddenException:
        raise SelfReviewForbiddenHTTPException

    except ReviewAlreadyExistsException:
        raise ReviewAlreadyExistsHTTPException

    except ObjectNotFoundException:
        raise ObjectNotFoundHTTPException
    return {"status": "OK"}


@router.get("")
async def get_all_reviews_by_user_id(
    db: DBDep,
    user_id: int
):
    try:
        formated_reviews = await ReviewService(db).get_all_reviews(user_id)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    return {"status": "OK", "data": formated_reviews}