from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse
from psycopg.rows import dict_row
from ulid import ULID

from api.auth_middleware import verify_token
from api.food.schema import (
    AddFoodReq,
    AllFoodsResp,
    DeleteFoodResp,
    Food,
    UpdateFoodReq,
    UpdateFoodResp,
)
from db import pool

food_router = APIRouter(prefix="/foods", tags=["foods"])


@food_router.get("/", response_model=AllFoodsResp)
def get_all_foods():
    try:
        with (
            pool.connection() as conn,
            conn.cursor(row_factory=dict_row) as cur,
        ):
            query = """
                SELECT * FROM foods;
            """
            foods = cur.execute(query).fetchall()

        return ORJSONResponse(
            content={
                "count": len(foods),
                "data": foods,
            },
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@food_router.get("/{id}", response_model=Food)
def get_by_id(id: str):
    try:
        with (
            pool.connection() as conn,
            conn.cursor(row_factory=dict_row) as cur,
        ):
            query = """
                SELECT * FROM foods WHERE id = %s;
            """
            food = cur.execute(query, [id], prepare=True).fetchone()

        return ORJSONResponse(
            content=food,
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@food_router.post("/", response_model=Food)
def add_new_food(id: str, req: AddFoodReq, payload=Depends(verify_token)):
    try:
        with (
            pool.connection() as conn,
            conn.transaction(),
            conn.cursor(row_factory=dict_row) as cur,
        ):
            query = """
                INSERT INTO foods
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id, image, name, description, price, review;
            """
            params = [
                str(ULID()),
                payload["id"],
                req.owner_id,
                req.location_id,
                req.image,
                req.name,
                req.description,
                req.price,
                req.review,
            ]
            food = cur.execute(query, params, prepare=True).fetchone()

        return ORJSONResponse(
            content=jsonable_encoder(food),
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@food_router.patch("/{id}", response_model=UpdateFoodResp)
def update_by_id(id: str, req: UpdateFoodReq):
    try:
        with (
            pool.connection() as conn,
            conn.transaction(),
            conn.cursor(row_factory=dict_row) as cur,
        ):
            cols = []
            params = []
            for col, val in req.model_dump().items():
                if val is not None:
                    cols.append(f"{col} = %s")
                    params.append(val)
            params.append(id)

            query = f"""
                UPDATE foods
                SET {", ".join(cols)}
                WHERE id = %s
                RETURNING *
            """

            food = cur.execute(query, params, prepare=True).fetchone()

        return ORJSONResponse(
            content={
                "message": "food is updated",
                "data": jsonable_encoder(food),
            },
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@food_router.delete("/{id}", response_model=DeleteFoodResp)
def delete_by_id(id: str):
    try:
        with (
            pool.connection() as conn,
            pool.transaction(),
            conn.cursor(row_factory=dict_row) as cur,
        ):
            query = """
                DELETE FROM foods WHERE id = %s
                RETURNING id, image, name, description, price, review;
            """
            food = cur.execute(query, [id], prepare=True).fetchone()

        return ORJSONResponse(
            content={
                "message": f"food with id={id} is deleted",
                "data": food,
            },
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
