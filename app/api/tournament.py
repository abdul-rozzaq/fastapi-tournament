from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.dependencies.database import get_db
from app.models.tournament import Tournament
from app.schemas.tournament import TournamentRead, TournamentCreate
from app.services.tournament import DBTournamentService


router = APIRouter(tags=["tournament"], prefix="/tournaments")

"""
@router.get("/", response_model=List[TournamentRead])
async def get_tournaments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tournament))
    tournaments = result.scalars().all()
    return tournaments

"""


@router.get("/", response_model=List[TournamentRead])
async def get_tournaments(service: DBTournamentService):
    return await service.get_all()


@router.get("/{id}", response_model=TournamentRead)
async def get_tournament(id: int, service: DBTournamentService):
    return await service.get_by_id(id)


@router.post("/", response_model=TournamentRead)
async def create_tournament(tournament: TournamentCreate, service: DBTournamentService):
    return await service.create(tournament)


@router.post("/{id}/register")
async def register_tournament():
    return


@router.post("/{id}/players")
async def tournament_players():
    return
