from fastapi import APIRouter

from app.dependencies.auth import CurrentUser
from app.schemas.tournament import TournamentCreate, TournamentRead
from app.schemas.user import UserRead
from app.services.tournament import DBTournamentService

router = APIRouter(tags=["tournament"], prefix="/tournaments")


@router.get("/", response_model=list[TournamentRead])
async def get_tournaments(current_user: CurrentUser, service: DBTournamentService):
    return await service.get_all()


@router.get("/{id}", response_model=TournamentRead)
async def get_tournament(current_user: CurrentUser, id: int, service: DBTournamentService):
    return await service.get_by_id(id)


@router.post("/", response_model=TournamentRead)
async def create_tournament(current_user: CurrentUser, tournament: TournamentCreate, service: DBTournamentService):
    return await service.create(user=current_user, tournament=tournament)


@router.post("/{id}/register")
async def register_tournament(id: int, current_user: CurrentUser, service: DBTournamentService):
    return await service.register(user_id=current_user.id, tournament_id=id)


@router.post("/{id}/players", response_model=list[UserRead])
async def tournament_players(id: int, current_user: CurrentUser, service: DBTournamentService):
    return await service.get_players(id)
