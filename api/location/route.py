from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse
from loguru import logger
from psycopg.rows import dict_row

from api.auth_middleware import verify_token
from api.location.schema import (
    AddLocationReq,
    AddLocationResp,
    Location,
    UpdateLocationReq,
    UpdateLocationResp,
)
from db import pool

location_router = APIRouter(
    prefix="/locations", tags=["locations"], dependencies=[Depends(verify_token)]
)


@location_router.get("/", response_model=list[Location])
def get_all_locations():
    try:
        with (
            pool.connection() as conn,
            conn.cursor(row_factory=dict_row) as cur,
        ):
            query = "SELECT * FROM locations;"
            locations = cur.execute(query, prepare=True).fetchall()

        if locations == []:
            return []

        return locations
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_200_OK, detail=str(e))


@location_router.get(
    "/{id}", response_model=Location | None
)
def get_by_id(id: str):
    try:
        with (
            pool.connection() as conn,
            conn.cursor(row_factory=dict_row) as cur,
        ):
            query = "SELECT * FROM locations WHERE id = %s"
            location = cur.execute(query, [id], prepare=True).fetchone()

        if location is None:
            return None

        return location
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@location_router.post(
    "/", response_model=AddLocationResp
)
def add_new_location(req: AddLocationReq):
    try:
        with (
            pool.connection() as conn,
            conn.transaction(),
            conn.cursor(row_factory=dict_row) as cur,
        ):
            query = """
                INSERT INTO locations
                VALUES(%s, %s, %s, %s, %s, %s)
                RETURNING *
            """
            params = [
                str(uuid4()),
                req.district,
                req.city,
                req.province,
                req.postal_code,
                req.details,
            ]
            location = cur.execute(query, params, prepare=True).fetchone()

        if location == {}:
            return ORJSONResponse(
                content={"message": "", "data": []},
                status_code=status.HTTP_201_CREATED,
            )

        return ORJSONResponse(
            content={
                "message": "location is created",
                "data": jsonable_encoder(location),
            },
            status_code=status.HTTP_201_CREATED,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@location_router.patch(
    "/{id}", response_model=UpdateLocationResp
)
def update_by_id(id: str, req: UpdateLocationReq):
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

            print(cols, flush=True)
            logger.info(cols)
            logger.info(params)

            query = f"""
                UPDATE locations
                SET {", ".join(cols)}
                WHERE id = %s
                RETURNING *
            """

            location = cur.execute(query, params, prepare=True).fetchone()

        if location is None:
            return ORJSONResponse(
                content={
                    "message": "not found",
                    "data": None,
                },
                status_code=status.HTTP_404_NOT_FOUND,
            )

        return ORJSONResponse(
            content={
                "message": "location is updated",
                "data": jsonable_encoder(location),
            },
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@location_router.delete(
    "/{id}", response_model=Location | None
)
def delete_by_id(id: str):
    try:
        with (
            pool.connection() as conn,
            conn.cursor(row_factory=dict_row) as cur,
        ):
            query = """
                DELETE FROM locations WHERE id = %s
                RETURNING *;
            """
            location = cur.execute(query, [id], prepare=True).fetchone()

        if location is None:
            return None

        return location
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
