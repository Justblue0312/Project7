import logging

from fastapi import APIRouter, Depends
from fastapi_sqlalchemy import db

from app.helpers.exception_handler import CustomException
from app.schemas.sche_base import DataResponse
from app.schemas.sche_sqlite import CreateDatabaseRequest, UserDatabaseResponse
from app.helpers.login_manager import login_required
from app.models import User
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
        new_db = ""
    except:
        pass
