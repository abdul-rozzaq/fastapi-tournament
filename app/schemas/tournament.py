from pydantic import BaseModel
from datetime import datetime


class TournamentBase(BaseModel):
    name: str
    max_players: int
    start_at: datetime


class TournamentCreate(TournamentBase):
    pass

    class Config:
        from_attributes = True


class TournamentRead(TournamentBase):
    id: int
