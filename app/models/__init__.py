# Import all the models, so that Base has them before being
from app.models.model_base import Base  # noqa
from app.models.model_sqilte import Sqlite  # noqa
from app.models.model_user import User  # noqa
