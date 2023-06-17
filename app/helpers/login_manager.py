from fastapi import Depends, HTTPException
from services.srv_user import UserService

from app.models import User


def login_required(
        http_authorization_credentials: str = Depends(UserService().reusable_oauth2),
):
    return UserService().get_current_user(http_authorization_credentials)


class PermissionRequired:
    def __init__(self, *args):
        self.user = None
        self.permissions = args

    def __call__(self, user: User = Depends(login_required)):
        self.user = user
        if self.user.role not in self.permissions and self.permissions:
            raise HTTPException(
                status_code=400,
                detail=f"User {self.user.email} can not access this API",
            )
