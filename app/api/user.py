from fastapi import APIRouter, HTTPException, status

from app.dependencies.auth import CurrentUser
from app.schemas.user import AuthResponse, UserCreate, UserLogin, UserRead
from app.services.user import DBUserService
from app.utils import create_access_token, verify_password

router = APIRouter(tags=["user"], prefix="/user")


@router.post("/login", response_model=AuthResponse)
async def login(data: UserLogin, service: DBUserService):
    user = await service.get_by_email(data.email)

    if not verify_password(data.password, user.hashed_password):  # type: ignore
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email yoki parol noto'g'ri")

    user_response = UserRead.model_validate(user)
    access_token = create_access_token(user_response.model_dump())

    return {"token": access_token, "user": user_response}


@router.post("/register", response_model=AuthResponse)
async def register(user: UserCreate, service: DBUserService):
    new_user = UserRead.model_validate(await service.create(user))
    access_token = create_access_token(new_user.model_dump())

    return {"user": new_user, "token": access_token}


@router.get("/me", response_model=UserRead)
async def me(currect_user: CurrentUser):
    return currect_user
