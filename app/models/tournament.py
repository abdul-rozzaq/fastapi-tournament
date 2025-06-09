from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Tournament(Base):
    __tablename__ = "tournaments"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    max_players = Column(Integer, nullable=False)
    start_at = Column(DateTime(timezone=True), nullable=False)

    registrations = relationship(
        "TournamentRegistration", back_populates="tournament", lazy="selectin"
    )

    __table_args__ = (
        CheckConstraint("max_players >= 1", "check_max_players_positive"),
    )


class TournamentRegistration(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    tournament_id = Column(Integer, ForeignKey("tournaments.id"))

    registered_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    user = relationship("User", back_populates="registrations")
    tournament = relationship("Tournament", back_populates="registrations")
