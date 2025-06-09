from app.database import Base

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    registrations = relationship("TournamentRegistration", back_populates="user")
