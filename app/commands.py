from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models
from .events import DomainEvent, publish


class DomainError(Exception):
    pass


class NotFound(DomainError):
    pass


class Conflict(DomainError):
    pass


def _exists(session: Session, model, column, value) -> bool:
    return session.scalar(select(model.id).where(column == value)) is not None


def create_league(session: Session, payload: dict) -> tuple[models.League, DomainEvent]:
    if _exists(session, models.League, models.League.name, payload["name"]):
        raise Conflict("league already exists")
    league = models.League(**payload)
    session.add(league)
    session.flush()
    event = DomainEvent("league.created", {"id": league.id, "name": league.name})
    publish(session, event)
    session.commit()
    return league, event


def create_club(session: Session, payload: dict) -> tuple[models.Club, DomainEvent]:
    if session.get(models.League, payload["league_id"]) is None:
        raise NotFound("league not found")
    if _exists(session, models.Club, models.Club.name, payload["name"]):
        raise Conflict("club already exists")
    club = models.Club(**payload)
    session.add(club)
    session.flush()
    event = DomainEvent(
        "club.created",
        {"id": club.id, "name": club.name, "league_id": club.league_id},
    )
    publish(session, event)
    session.commit()
    return club, event


def create_player(session: Session, payload: dict) -> tuple[models.Player, DomainEvent]:
    if session.get(models.Club, payload["club_id"]) is None:
        raise NotFound("club not found")
    player = models.Player(**payload)
    session.add(player)
    session.flush()
    event = DomainEvent(
        "player.created",
        {"id": player.id, "name": player.name, "club_id": player.club_id},
    )
    publish(session, event)
    session.commit()
    return player, event
