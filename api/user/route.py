from datetime import datetime, timedelta, timezone
from uuid import uuid4

import bcrypt
import jwt
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from psycopg.rows import dict_row

from api.user.schema import LoginReq, LoginResp, RegisterReq, RegisterResp
from db import pool

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/register", response_model=RegisterResp)
def register(req: RegisterReq):
    try:
        with (
            pool.connection() as conn,
            conn.transaction(),
            conn.cursor(row_factory=dict_row) as cur,
        ):
            query = """
                INSERT INTO users
                VALUES(%s, %s, %s, %s, %s, %s)
                RETURNING username, email
            """
            params = [
                str(uuid4()),
                req.profile_picture,
                req.username,
                req.email,
                req.fullname,
                bcrypt.hashpw(req.password.encode(), bcrypt.gensalt()).decode(),
            ]
            user = cur.execute(query, params, prepare=True).fetchone()

        return {"message": "user is registered", "data": user}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@user_router.post("/login", response_model=LoginResp | None)
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
                return JSONResponse(content={"token": None})

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
                    key="secret",
                    algorithm="HS256",
                )
                return JSONResponse(content={"token": token_jwt})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
