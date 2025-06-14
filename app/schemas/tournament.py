from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.registration import RegistrationRead


class TournamentBase(BaseModel):
    name: str
    max_players: int = Field(ge=1)
    start_at: datetime


class TournamentCreate(TournamentBase):
    pass

    class Config:
        from_attributes = True


class TournamentRead(TournamentBase):
    id: int
    registrations: list[RegistrationRead] = []

    class Config:
        from_attributes = True
