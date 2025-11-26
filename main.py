from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from scalar_fastapi import get_scalar_api_reference

from api.user.route import user_router
from db import pool

app = FastAPI(summary="Kumande App", description="Kumande App")
app.include_router(user_router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    pool.open()

    yield

    pool.close()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"error": exc.errors(), "body": exc.body}),
    )


@app.get("/", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        title="Kumande API",
        openapi_url=app.openapi_url,
        scalar_proxy_url="https://proxy.scalar.com",
    )
