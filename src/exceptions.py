from fastapi import HTTPException

class FreelanceExceptions(Exception):
    detail = "Неизвестная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, args, **kwargs)

class RoleNotFoundException(FreelanceExceptions):
    detail = "Неизвестная роль"

class ObjectNotFoundException(FreelanceExceptions):
    detail = "Объект не найден"

class UserNotFoundException(FreelanceExceptions):
    detail = "Такого пользователя не существует"

class UserAlreadyExistsException(FreelanceExceptions):
    detail = "Пользователь уже существует"

class WrongPasswordException(FreelanceExceptions):
    detail = "Неверный пароль"

class PermissionDeniedException(FreelanceExceptions):
    detail = "Доступ запрещен"

class OrderNotInProgressException(FreelanceExceptions):
    detail = "Заказ не находится в процессе выполнения"

class AlreadyRespondedException(FreelanceExceptions):
    detail = "Вы уже откликнулись на этот заказ"

class AlreadyAcceptedException(FreelanceExceptions):
    detail = "Заказ уже принят"

class AlreadyRejectedException(FreelanceExceptions):
    detail = "Заказ уже отклонен"

class InvalidReviewParticipantsException(FreelanceExceptions):
    detail = "Отзыв может быть оставлен только между участниками заказа"

class ReviewCommentRequiredException(FreelanceExceptions):
    detail = "Для оценки ниже 5 необходимо оставить комментарий"

class OrderNotCompletedException(FreelanceExceptions):
    detail = "Нельзя оставить отзыв на незавершённый заказ"

class SelfReviewForbiddenException(FreelanceExceptions):
    detail = "Нельзя оставить отзыв самому себе"

class ReviewAlreadyExistsException(FreelanceExceptions):
    detail = "Вы уже оставили отзыв на этот заказ"

class UserAlreadyHasRoleException(FreelanceExceptions):
    detail = "Пользователь уже имеет данную роль"

class UserIsBlockedException(FreelanceExceptions):
    detail = "Ваш аккаунт заблокирован"


class FreelanceHTTPExceptions(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class ObjectNotFoundHTTPException(FreelanceHTTPExceptions):
    status_code = 404
    detail = "Объект не найден"

class UserNotFoundHTTPException(FreelanceHTTPExceptions):
    status_code = 404
    detail = "Такого пользователя не существует"

class WrongPasswordHTTPException(FreelanceHTTPExceptions):
    status_code = 401
    detail = "Неправильный пароль"

class PermissionDeniedHTTPException(FreelanceHTTPExceptions):
    status_code = 403
    detail = "Доступ запрещен"

class OrderNotInProgressHTTPException(FreelanceHTTPExceptions):
    status_code = 409
    detail = "Заказ не находится в процессе выполнения"

class AlreadyRespondedHTTPException(FreelanceHTTPExceptions):
    status_code = 409
    detail = "Вы уже откликнулись на этот заказ"

class AlreadyAcceptedHTTPException(FreelanceHTTPExceptions):
    status_code = 409
    detail = "Заказ уже принят"

class AlreadyRejectedHTTPException(FreelanceHTTPExceptions):
    status_code = 409
    detail = "Заказ уже отклонен"

class InvalidReviewParticipantsHTTPException(FreelanceHTTPExceptions):
    status_code = 400
    detail = "Отзыв может быть оставлен только между участниками заказа"

class ReviewCommentRequiredHTTPException(FreelanceHTTPExceptions):
    status_code = 400
    detail = "Для оценки ниже 5 необходимо оставить комментарий"

class OrderNotCompletedHTTPException(FreelanceHTTPExceptions):
    status_code = 400
    detail = "Нельзя оставить отзыв на незавершённый заказ"

class SelfReviewForbiddenHTTPException(FreelanceHTTPExceptions):
    status_code = 400
    detail = "Нельзя оставить отзыв самому себе"

class ReviewAlreadyExistsHTTPException(FreelanceHTTPExceptions):
    status_code = 409
    detail = "Вы уже оставили отзыв на этот заказ"

class UserAlreadyHasRoleHTTPException(FreelanceHTTPExceptions):
    status_code = 409
    detail = "Пользователь уже имеет данную роль"

class UserIsBlockedHTTPException(FreelanceHTTPExceptions):
    status_code = 403
    detail = "Ваш аккаунт заблокирован"

class UserAlreadyExistsHTTPException(FreelanceHTTPExceptions):
    status_code = 409
    detail = "Пользоватль уже существует"
