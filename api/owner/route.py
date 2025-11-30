from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse
from psycopg.rows import dict_row
from ulid import ULID

from api.auth_middleware import verify_token
from api.owner.schema import AddOwnerReq, AddOwnerResp, AllOwnersResp
from db import pool

owner_router = APIRouter(
    prefix="/owners",
    tags=["owners"],
    dependencies=[Depends(verify_token)],
)


@owner_router.post(
    "/",
    response_model=AddOwnerResp,
)
def add_new_owner(req: AddOwnerReq):
    try:
        with (
            pool.connection() as conn,
            conn.transaction(),
            conn.cursor(row_factory=dict_row) as cur,
        ):
            query = """
                INSERT INTO owners
                VALUES(%s, %s, %s)
                RETURNING id, image, name;
            """
            params = [str(ULID()), req.image, req.name]
            owner = cur.execute(query, params, prepare=True).fetchone()

        return ORJSONResponse(
            content={
                "data": jsonable_encoder(owner),
            },
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@owner_router.get(
    "/",
    response_model=AllOwnersResp,
)
def get_all():
    try:
        with pool.connection() as conn, conn.cursor(row_factory=dict_row) as cur:
            query = """
                SELECT id, image, name FROM owners;
            """
            owners = cur.execute(query).fetchall()

        return ORJSONResponse(
            content={
                "count": len(owners),
                "data": jsonable_encoder(owners),
            },
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@owner_router.get("/{id}", response_model=AddOwnerResp)
def get_by_id(id: str):
    try:
        with pool.connection() as conn, conn.cursor(row_factory=dict_row) as cur:
            query = """
                SELECT id, images, name FROM owners WHERE id = %s;
            """
            owners = cur.execute(query, [id]).fetchall()

        return ORJSONResponse(
            content={
                "data": jsonable_encoder(owners),
            },
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@owner_router.patch("/{id}", response_model=AddOwnerResp)
def update_by_id(id: str, req: AddOwnerReq):
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
                UPDATE owners
                SET {", ".join(cols)}
                WHERE id = %s
                RETURNING *
            """
            owner = cur.execute(query, params, prepare=True).fetchone()

        return ORJSONResponse(
            content={
                "data": jsonable_encoder(owner),
            },
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@owner_router.delete("/{id}")
def delete_by_id(id: str):
    try:
        with (
            pool.connection() as conn,
            conn.cursor(row_factory=dict_row) as cur,
        ):
            query = """
                DELETE FROM owners WHERE id = %s
                RETURNING *;
            """
            location = cur.execute(query, [id], prepare=True).fetchone()

        if location is None:
            return None

        return location
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
