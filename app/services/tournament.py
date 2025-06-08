from typing import Annotated, List
from fastapi import Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.dependencies.database import get_db
from app.models.tournament import Tournament
from app.schemas.tournament import TournamentCreate, TournamentRead


class TournamentService:

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, tournament: TournamentCreate):
        new_tournament = Tournament(**tournament.model_dump())

        self.db.add(new_tournament)
        await self.db.commit()
        await self.db.refresh(new_tournament)

        return new_tournament

    async def get_all(self):
        result = await self.db.execute(select(Tournament))
        tournaments = result.scalars().all()

        return tournaments

    async def get_by_id(self, id) -> Tournament:
        result = await self.db.execute(select(Tournament).filter(Tournament.id == id))
        tournament = result.scalars().first()

        if not tournament:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Tournament not found")

        return tournament


def get_tournament_service(db: AsyncSession = Depends(get_db)):
    return TournamentService(db)


DBTournamentService = Annotated[TournamentService, Depends(get_tournament_service)]
