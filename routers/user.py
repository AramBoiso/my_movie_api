from fastapi import APIRouter
from fastapi.responses import JSONResponse
from utils.jwt_manager import generate_token
from schemas.user import User

user_router = APIRouter()


@user_router.post('/login', tags=['Auth'], response_model=User, status_code=200)
def login(user: User) -> User:
    if user.email == "admin@admin.com" and user.password == "admin":
        return JSONResponse(status_code=200, content={
            "token": generate_token(user.model_dump())
        })
    return JSONResponse(status_code=401, content={
        "message": "Unauthorized"
    })