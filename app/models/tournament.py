from sqlalchemy import Column, String, Integer, CheckConstraint, DateTime

from app.database import Base


class Tournament(Base):
    __tablename__ = "tournaments"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    max_players = Column(Integer, nullable=False)
    start_at = Column(DateTime, nullable=False)

    __table_args__ = (CheckConstraint("max_players >= 1", "check_max_players_positive"),)
