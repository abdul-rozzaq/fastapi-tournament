from app import database


async def get_db():
    async with database.AsyncSessionLocal() as session:  # type: ignore
        yield session
