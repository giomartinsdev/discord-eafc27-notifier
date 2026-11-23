from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, Index, String, func
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class League(Base):
    __tablename__ = "leagues"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    country: Mapped[str] = mapped_column(String(80), index=True)


class Club(Base):
    __tablename__ = "clubs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    league_id: Mapped[int] = mapped_column(ForeignKey("leagues.id", ondelete="CASCADE"))
    overall: Mapped[int] = mapped_column(default=0)
    attack: Mapped[int] = mapped_column(default=0)
    midfield: Mapped[int] = mapped_column(default=0)
    defense: Mapped[int] = mapped_column(default=0)
    budget: Mapped[int] = mapped_column(default=0)

    __table_args__ = (Index("ix_clubs_league_overall", "league_id", "overall"),)


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    club_id: Mapped[int] = mapped_column(ForeignKey("clubs.id", ondelete="CASCADE"))
    position: Mapped[str] = mapped_column(String(8), index=True)
    overall: Mapped[int] = mapped_column(default=0)
    age: Mapped[int] = mapped_column(default=0)

    __table_args__ = (Index("ix_players_club_overall", "club_id", "overall"),)


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(64), index=True)
    payload: Mapped[dict] = mapped_column(JSON)
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
