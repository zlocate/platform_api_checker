from fastapi import APIRouter, HTTPException, Depends

from app.core.logger import CustomLogger
from app.core.stand_creator import StandCreator
from app.models.create_stand_request import CreateStandRequest
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.config import Config

router = APIRouter()
logger = CustomLogger()
security = HTTPBasic()


def basic_auth(
    required: bool = Config.get_is_basic_auth_required(),
    credentials: HTTPBasicCredentials = Depends(security),
    username: str = Config.get_basic_auth_username(),
    password: str = Config.get_basic_auth_password()
): 

    if not required:
        return
    
    provided_username = credentials.username
    provided_password = credentials.password

    if provided_username != username or provided_password != password:
        raise HTTPException(
            status_code=401,
            detail="Authorization required",
            headers={"WWW-Authenticate": "Basic"},
        )

    return str(provided_username)


@router.post("/stand")
def create_post(post: CreateStandRequest, _ = Depends(basic_auth)):
    logger.message(f"Запрос на ручку stand {post}")
    stand_creator = StandCreator()
    return stand_creator.create_stand_handler(post)