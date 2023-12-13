from fastapi import APIRouter, Depends

from app.core.logger import CustomLogger
from app.core.stand_creator import StandCreator
from app.models.create_stand_request import CreateStandRequest

router = APIRouter()
logger = CustomLogger()

@router.post("/stand")
def create_post(post: CreateStandRequest):
    logger.message(f"Запрос на ручку stand {post}")
    stand_creator = StandCreator()
    return stand_creator.create_stand_handler(post)