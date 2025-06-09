from datetime import UTC, datetime, timedelta

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.dependencies.database import get_db
from app.main import app
from app.models.tournament import Tournament, TournamentRegistration
from app.models.user import User

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest_asyncio.fixture(autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(User.metadata.create_all)
        await conn.run_sync(Tournament.metadata.create_all)
        await conn.run_sync(TournamentRegistration.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(User.metadata.drop_all)
        await conn.run_sync(Tournament.metadata.drop_all)
        await conn.run_sync(TournamentRegistration.metadata.drop_all)


@pytest_asyncio.fixture
async def access_token():
    response = client.post("/user/register", json={"name": "Sanjar", "email": "test@example.com", "password": "testpassword"})
    assert response.status_code == 200
    return response.json()["token"]


@pytest_asyncio.fixture
async def test_tournament():
    async with TestingSessionLocal() as session:
        tournament = Tournament(name="Test Tournament", max_players=10, start_at=datetime.now(UTC) + timedelta(days=1))
        session.add(tournament)
        await session.commit()
        await session.refresh(tournament)
        return tournament


@pytest.mark.asyncio
async def test_register_user():
    response = client.post("/user/register", json={"name": "Shoxruh", "email": "newuser@example.com", "password": "newpassword"})
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["name"] == "Shoxruh"
    assert data["user"]["email"] == "newuser@example.com"
    assert "token" in data


@pytest.mark.asyncio
async def test_create_tournament(access_token):
    tournament_data = {"name": "New Tournament", "max_players": 10, "start_at": (datetime.now(UTC) + timedelta(days=1)).isoformat()}
    response = client.post("/tournaments/", json=tournament_data, headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Tournament"
    assert data["max_players"] == 10
    assert len(data["registrations"]) == 1


@pytest.mark.asyncio
async def test_register_existing_tournament(access_token, test_tournament):
    response = client.post(f"/tournaments/{test_tournament.id}/register", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_register_already_registered_tournament(access_token, test_tournament):

    response = client.post(f"/tournaments/{test_tournament.id}/register", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200

    response = client.post(f"/tournaments/{test_tournament.id}/register", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Siz allaqachon ro'yhatdan o'tgansiz"
