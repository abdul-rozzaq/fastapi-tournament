
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.dependencies.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils import get_password_hash


class UserService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, user: UserCreate) -> User:
        hashed_password = get_password_hash(user.password)

        result = await self.db.execute(select(User).filter(User.email == user.email))
        exist_user = result.scalars().first()

        if exist_user:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "User with this email already exists")

        new_user = User(name=user.name, email=user.email, hashed_password=hashed_password)

        self.db.add(new_user)

        await self.db.commit()
        await self.db.refresh(new_user)

        return new_user

    async def get_by_email(self, email: str) -> User:
        result = await self.db.execute(select(User).filter(User.email == email))
        user = result.scalars().first()

        if not user:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Email yoki parol noto'g'ri")

        return user


def get_user_service(db: AsyncSession = Depends(get_db)):
    return UserService(db)  # type: ignore


DBUserService = Annotated[UserService, Depends(get_user_service)]
