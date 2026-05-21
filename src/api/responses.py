from fastapi import APIRouter
from src.api.dependencies import DBDep, CurrentUserDep
from src.exceptions import PermissionDeniedException, PermissionDeniedHTTPException
from src.services.responses import ResponsesService

router = APIRouter(prefix="/response", tags=["Отклики"])


@router.get("/my")
async def get_all_my_responses(db: DBDep, current_user: CurrentUserDep):
    try:
        result = await ResponsesService(db).get_all_my_responses(
            current_user.role, current_user.id
        )
    except PermissionDeniedException:
        raise PermissionDeniedHTTPException

    return {"status": "OK", "data": result}
