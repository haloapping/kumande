from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from scalar_fastapi import get_scalar_api_reference

from api.location.route import location_router
from api.owner.route import owner_router
from api.user.route import user_router
from api.food.route import food_router
from db import pool

app = FastAPI(summary="Kumande App", description="Kumande App")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await pool.open()

    yield

    await pool.close()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=jsonable_encoder({"error": exc.errors(), "body": exc.body}),
    )


@app.get("/", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        title="Kumande API",
        openapi_url=app.openapi_url,
        scalar_proxy_url="https://proxy.scalar.com",
    )


app.include_router(user_router)
app.include_router(location_router)
app.include_router(owner_router)
app.include_router(food_router)
