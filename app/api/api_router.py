from fastapi import APIRouter

from app.api import api_healthcheck, api_login, api_register, api_user

router = APIRouter()

router.include_router(
    api_healthcheck.router, tags=["health-check"], prefix="/healthcheck"
)
router.include_router(api_login.router, tags=["login"], prefix="/login")
router.include_router(api_register.router, tags=["register"], prefix="/register")
router.include_router(api_user.router, tags=["user"], prefix="/users")
