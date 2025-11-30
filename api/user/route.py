import os
from datetime import datetime, timedelta, timezone
from typing import Final

import bcrypt
import jwt
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import ORJSONResponse
from psycopg.rows import dict_row
from ulid import ULID

from api.user.schema import LoginReq, LoginResp, RegisterReq, RegisterResp
from db import pool

load_dotenv()
JWT_SECRET_KEY: Final = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM: Final = os.getenv("JWT_ALGORITHM")

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post(
    "/register",
    response_class=ORJSONResponse,
    response_model=RegisterResp,
)
def register(req: RegisterReq):
    try:
        with (
            pool.connection() as conn,
            conn.transaction(),
            conn.cursor(row_factory=dict_row) as cur,
        ):
            query = """
                INSERT INTO users
                VALUES(%s, %s, %s, %s, %s)
                RETURNING username, email
            """
            params = [
                str(ULID()),
                req.profile_picture,
                req.username,
                req.email,
                bcrypt.hashpw(req.password.encode(), bcrypt.gensalt()).decode(),
            ]
            user = cur.execute(query, params, prepare=True).fetchone()

        return ORJSONResponse(
            content={
                "message": "user is registered",
                "data": user,
            },
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@user_router.post(
    "/login",
    response_class=ORJSONResponse,
    response_model=LoginResp | None,
)
def login(req: LoginReq):
    try:
        with (
            pool.connection() as conn,
            conn.cursor(row_factory=dict_row) as cur,
        ):
            query = """
                SELECT id, username, password FROM users WHERE username = %s;
            """
            user = cur.execute(query, [req.username], prepare=True).fetchone()

            if user is None:
                return ORJSONResponse(
                    content={"token": None},
                    status_code=status.HTTP_200_OK,
                )

            is_password_match = bcrypt.checkpw(
                req.password.encode(), str(user["password"]).encode()
            )
            if is_password_match:
                token_jwt = jwt.encode(
                    payload={
                        "id": user["id"],
                        "iat": datetime.now(timezone.utc),
                        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
                    },
                    key=JWT_SECRET_KEY,
                    algorithm=JWT_ALGORITHM,
                )
                return ORJSONResponse(
                    content={"token": token_jwt},
                    status_code=status.HTTP_200_OK,
                )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
