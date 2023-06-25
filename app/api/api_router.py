from fastapi import APIRouter

from app.api import (api_healthcheck, api_login, api_register, api_sqlite,
                     api_user)

router = APIRouter()

router.include_router(
    api_healthcheck.router, tags=["Health-Check"], prefix="/healthcheck"
)
router.include_router(api_login.router, tags=["Login"], prefix="/login")
router.include_router(api_register.router, tags=["Register"], prefix="/register")
router.include_router(api_user.router, tags=["User"], prefix="/users")
router.include_router(api_sqlite.router, tags=["DB"], prefix="/db")
