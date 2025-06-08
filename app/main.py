from fastapi import FastAPI

from .api import user, tournament


app = FastAPI()


app.include_router(user.router)
app.include_router(tournament.router)
