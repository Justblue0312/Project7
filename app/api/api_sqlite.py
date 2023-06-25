import logging
from typing import Any

from fastapi import APIRouter, Depends

from app.helpers.exception_handler import CustomException
from app.helpers.login_manager import login_required
from app.models import User
from app.schemas.sche_base import DataResponse
from app.schemas.sche_sqlite import CreateDatabaseRequest, UserDatabaseResponse
from app.services.srv_sqlite import SqliteService
from app.services.srv_user import UserService

logger = logging.getLogger()
router = APIRouter()


@router.post(
    "/create",
    dependencies=[Depends(login_required)],
    response_model=DataResponse[UserDatabaseResponse],
)
def create_user_db(
    request: CreateDatabaseRequest,
    current_user: User = Depends(UserService().get_current_user),
):
    try:
        if not request.db_name:
            raise CustomException(
                http_code=400, code="400", message="Invalid database name"
            )
        new_db = SqliteService.create_database(current_user, request)
        user_db_res = UserDatabaseResponse(**new_db.to_dict())
        return DataResponse().success_response(data=user_db_res)
    except Exception as e:
        raise CustomException(http_code=400, code="400", message=str(e))
