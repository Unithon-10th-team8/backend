from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from app.exception_handlers import add_exception_handlers


def init_views(app: FastAPI) -> None:
    from app.views import router as v1_router

    @app.get("/")
    def ping() -> str:
        return "pong"

    app.include_router(v1_router, prefix="/v1")


def create_app() -> FastAPI:
    """FastAPI 앱을 생성합니다."""

    app = FastAPI(
        openapi_url="/openapi.json",
        default_response_class=ORJSONResponse,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    add_exception_handlers(app)
    init_views(app)

    @app.on_event("startup")
    async def startup() -> None:
        """서버 실행시 이벤트를 넣어주세요."""
        pass

    @app.on_event("shutdown")
    async def shutdown() -> None:
        """서버 종료시 이벤트를 넣어주세요."""
        pass

    return app


app = create_app()
