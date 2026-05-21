from datetime import datetime

from fastapi import APIRouter, Response, Body

from src.api.dependencies import DBDep, CurrentUserDep
from src.celery_tasks.tasks import create_report_exel, create_report_pdf
from src.exceptions import ObjectNotFoundException, WrongPasswordException, ObjectNotFoundHTTPException, \
    WrongPasswordHTTPException, PermissionDeniedHTTPException, PermissionDeniedException, UserIsBlockedException, \
    UserIsBlockedHTTPException, UserAlreadyExistsException, UserAlreadyExistsHTTPException
from src.schemas.user import UserAddRequest, UserLogin, UserPatch
from src.services.auths import AuthenticationService

router = APIRouter(prefix="/auth", tags=["Аунтефикация и Авторизация"])

@router.post("/register")
async def register(
    data: UserAddRequest,
    db: DBDep,
):
    try:
        await AuthenticationService(db).register(data)
    except UserAlreadyExistsException:
        raise UserAlreadyExistsHTTPException

    return {"status": "OK"}


@router.post("/login")
async def login(
    db: DBDep,
    response: Response,
    data: UserLogin = Body(openapi_examples={
            "1": {
                "summary": "Тест 1(Customer)",
                "value": {"email": "karate@gmail.com", "password": "RoyalOAK"},
            },
            "2": {
                "summary": "Тест 2(Freelancer)",
                "value": {"email": "kot@pes.ru", "password": "AudemarPigue"},
            },
            "3": {
                "summary": "Тест 3(Administrator)",
                "value": {"email": "avadakedavra@pes.cot", "password": "RolexDateJust"},
            },
        })
):
    try:
        access_token = await AuthenticationService(db).login(data,response)
    except WrongPasswordException:
        raise WrongPasswordHTTPException
    except ObjectNotFoundException:
        raise ObjectNotFoundHTTPException
    except UserIsBlockedException:
        raise UserIsBlockedHTTPException
    return {"access_token": access_token}


@router.get("/get_me")
async def get_me(
    db: DBDep,
    current_user: CurrentUserDep
):
    result = await AuthenticationService(db).get_me(current_user)
    return {"data": result}


@router.post("/report/xlsx")
async def create_exel_report(
    date_from: datetime,
    date_to: datetime,
    current_user: CurrentUserDep,
):
    create_report_exel.delay(
        date_from.isoformat(),
        date_to.isoformat(),
        current_user.id,
        current_user.role,
        current_user.email,
        current_user.first_name,
        current_user.middle_name,
        current_user.last_name,
        current_user.rating
    )

    return {"status": "OK"}


@router.post("/report/pdf")
async def create_pdf_report(
    date_from: datetime,
    date_to: datetime,
    current_user: CurrentUserDep,
):
    create_report_pdf.delay(
        date_from.isoformat(),
        date_to.isoformat(),
        current_user.id,
        current_user.role,
        current_user.email,
        current_user.first_name,
        current_user.middle_name,
        current_user.last_name,
        current_user.rating
    )

    return {"status": "OK"}


@router.patch("/me")
async def partially_update_profile(
    db: DBDep,
    data: UserPatch,
    current_user: CurrentUserDep,
):
    try:
        await AuthenticationService(db).partially_update_profile(current_user.id, data)
    except PermissionDeniedException:
        raise PermissionDeniedHTTPException
    return {"status": "OK"}


@router.post("/logout")
async def logout(
    db: DBDep,
    response: Response
):
    await AuthenticationService(db).logout(response)
    return {"status": "OK"}