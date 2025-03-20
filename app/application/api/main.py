from fastapi import FastAPI

from application.api.static_docs import register_static_docs_routes
from application.api.v1.health import router as health_router_v1
from application.api.v1.messages.handlers import router as message_router_v1


def create_app() -> FastAPI:
    fastapi_app = FastAPI(
        title="Chat API",
        debug=True,
        docs_url=None,
        redoc_url=None,
    )

    register_static_docs_routes(app=fastapi_app)

    fastapi_app.include_router(prefix="/v1", router=message_router_v1)
    fastapi_app.include_router(prefix="/v1", router=health_router_v1)

    return fastapi_app
