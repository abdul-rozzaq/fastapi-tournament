from datetime import datetime

from pydantic import BaseModel


class RegistrationBase(BaseModel):
    user_id: int
    tournament_id: int


class RegistrationCreate(RegistrationBase):
    pass


class RegistrationRead(RegistrationBase):
    id: int
    registered_at: datetime
