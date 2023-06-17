from fastapi import APIRouter, Depends
from models import User
from services.srv_user import UserService

from app.schemas.sche_base import ResponseSchemaBase

router = APIRouter()


@router.get("", response_model=ResponseSchemaBase)
async def get():
    return {"message": "Health check success"}


@router.get("/protected_route", response_model=ResponseSchemaBase)
async def protected_route(current_user: User = Depends(UserService().get_current_user)):
    return {"message": "You are authenticated!"}
