from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models


def list_leagues(session: Session) -> list[models.League]:
    return list(session.scalars(select(models.League).order_by(models.League.name)))


def list_clubs(
    session: Session,
    league_id: int | None = None,
    min_overall: int | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[models.Club]:
    stmt = select(models.Club).order_by(models.Club.overall.desc(), models.Club.id)
    if league_id is not None:
        stmt = stmt.where(models.Club.league_id == league_id)
    if min_overall is not None:
        stmt = stmt.where(models.Club.overall >= min_overall)
    return list(session.scalars(stmt.limit(limit).offset(offset)))


def get_club(session: Session, club_id: int) -> models.Club | None:
    return session.get(models.Club, club_id)


def list_players(
    session: Session,
    club_id: int | None = None,
    min_overall: int | None = None,
    position: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[models.Player]:
    stmt = select(models.Player).order_by(models.Player.overall.desc(), models.Player.id)
    if club_id is not None:
        stmt = stmt.where(models.Player.club_id == club_id)
    if min_overall is not None:
        stmt = stmt.where(models.Player.overall >= min_overall)
    if position is not None:
        stmt = stmt.where(models.Player.position == position)
    return list(session.scalars(stmt.limit(limit).offset(offset)))


def list_events(session: Session, limit: int = 100) -> list[models.Event]:
    return list(session.scalars(select(models.Event).order_by(models.Event.id).limit(limit)))
