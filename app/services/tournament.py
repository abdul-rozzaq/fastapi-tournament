from datetime import UTC, datetime
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.dependencies.database import get_db
from app.models.tournament import Tournament, TournamentRegistration
from app.models.user import User
from app.schemas.tournament import TournamentCreate


class TournamentService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, user: User, tournament: TournamentCreate):
        new_tournament = Tournament(**tournament.model_dump())

        self.db.add(new_tournament)
        await self.db.commit()
        await self.db.refresh(new_tournament)

        #! Tournament yaratgan odamni o'zi ham tournamentga qo'shilyapti
        await self.register(user_id=user.id, tournament_id=new_tournament.id)

        await self.db.refresh(new_tournament)

        return new_tournament

    async def get_all(self):
        result = await self.db.execute(select(Tournament))
        tournaments = result.scalars().all()

        return tournaments

    async def get_by_id(self, id, raise_exception=True) -> Tournament:
        result = await self.db.execute(select(Tournament).filter(Tournament.id == id))
        tournament = result.scalar_one_or_none()

        if raise_exception and not tournament:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Tournament not found")

        return tournament

    async def register(self, user_id, tournament_id) -> TournamentRegistration:
        tournament = await self.get_by_id(tournament_id)

        await self.check_registration_validity(tournament, user_id)

        registration = TournamentRegistration(user_id=user_id, tournament_id=tournament_id)

        self.db.add(registration)

        await self.db.commit()
        await self.db.refresh(registration)

        return registration

    async def check_registration_validity(self, tournament: Tournament, user_id: int):
        # if tournament.start_at < datetime.now(UTC):
        if tournament.start_at < datetime.now(UTC).replace(tzinfo=None):
            raise HTTPException(400, "Tournament allaqachon boshlangan")

        if tournament.max_players <= len(tournament.registrations):
            raise HTTPException(400, "Max qatnashchi soniga yetilgan")

        if await self.get_registration(user_id, tournament.id):
            raise HTTPException(400, "Siz allaqachon ro'yhatdan o'tgansiz")

    async def get_registration(self, user_id, tournament_id):
        result = await self.db.execute(
            select(TournamentRegistration).where(
                TournamentRegistration.user_id == user_id,
                TournamentRegistration.tournament_id == tournament_id,
            )
        )
        registration = result.scalar_one_or_none()

        return registration

    async def get_players(self, id) -> list[User]:
        stmt = select(User).join(TournamentRegistration).where(TournamentRegistration.tournament_id == id)

        result = await self.db.execute(stmt)
        users = result.scalars().all()

        return users


def get_tournament_service(db: AsyncSession = Depends(get_db)):
    return TournamentService(db)


DBTournamentService = Annotated[TournamentService, Depends(get_tournament_service)]
