from app.clients.gitlab_client import GitlabClient
from app.core.logger import CustomLogger
from app.core.stand_creator import StandCreator
from app.routers import create_stand
from fastapi import FastAPI, Depends
import sentry_sdk

app = FastAPI()

sentry_sdk.init(
    dsn="https://b0f3a40208402c81879a79fe8bab4992@o4506372955176960.ingest.sentry.io/4506372988272640",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

gitlab_client = GitlabClient()
StandCreator(gitlab_client)
CustomLogger()


app.include_router(create_stand.router)
