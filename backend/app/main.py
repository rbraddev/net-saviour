from fastapi import FastAPI

from app.api import auth, ping


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(ping.router)
    application.include_router(auth.router, prefix="/auth", tags=["auth"])

    return application


app = create_application()
