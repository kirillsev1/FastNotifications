from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from src.api.v1.auth.router import auth_router
from src.api.v1.note.router import note_router
from src.api.v1.user.router import user_router
from src.on_startup.cors import add_cors


def setup_routers(app: FastAPI) -> None:
    routers = [
        auth_router,
        note_router,
        user_router,
    ]
    for router in routers:
        app.include_router(router)


def setup_middleware(app: FastAPI) -> None:
    # app.add_middleware(
    #     LogServerMiddleware,
    # )

    ...


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:

    yield

    return


def create_app() -> FastAPI:
    app = FastAPI(docs_url='/swagger', lifespan=lifespan)
    setup_routers(app)
    setup_middleware(app)
    add_cors(app)

    return app
