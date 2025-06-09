from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError

from app.config import ALGORITHM, SECRET_KEY
from app.models.user import User
from app.services.user import DBUserService

bearer_scheme = HTTPBearer()


async def get_current_user(service: DBUserService, credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)]):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])

        email = payload.get("email")

        if not email:
            raise credentials_exception

    except InvalidTokenError:
        raise credentials_exception from None

    user = await service.get_by_email(email)
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
