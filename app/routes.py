from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from . import queries
from .commands import Conflict, NotFound, create_club, create_league, create_player
from .db import get_session
from .events import dispatch
from .schemas import ClubIn, ClubOut, EventOut, LeagueIn, LeagueOut, PlayerIn, PlayerOut

router = APIRouter()


@router.post("/leagues", response_model=LeagueOut, status_code=201)
def post_league(data: LeagueIn, session: Session = Depends(get_session)):
    try:
        entity, event = create_league(session, data.model_dump())
    except Conflict as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    dispatch(event)
    return entity


@router.get("/leagues", response_model=list[LeagueOut])
def get_leagues(session: Session = Depends(get_session)):
    return queries.list_leagues(session)


@router.post("/clubs", response_model=ClubOut, status_code=201)
def post_club(data: ClubIn, session: Session = Depends(get_session)):
    try:
        entity, event = create_club(session, data.model_dump())
    except NotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Conflict as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    dispatch(event)
    return entity


@router.get("/clubs", response_model=list[ClubOut])
def get_clubs(
    league_id: int | None = None,
    min_overall: int | None = Query(default=None, ge=0, le=99),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    session: Session = Depends(get_session),
):
    return queries.list_clubs(session, league_id, min_overall, limit, offset)


@router.get("/clubs/{club_id}", response_model=ClubOut)
def get_club(club_id: int, session: Session = Depends(get_session)):
    club = queries.get_club(session, club_id)
    if club is None:
        raise HTTPException(status_code=404, detail="club not found")
    return club


@router.post("/players", response_model=PlayerOut, status_code=201)
def post_player(data: PlayerIn, session: Session = Depends(get_session)):
    try:
        entity, event = create_player(session, data.model_dump())
    except NotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    dispatch(event)
    return entity


@router.get("/players", response_model=list[PlayerOut])
def get_players(
    club_id: int | None = None,
    min_overall: int | None = Query(default=None, ge=0, le=99),
    position: str | None = None,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    session: Session = Depends(get_session),
):
    return queries.list_players(session, club_id, min_overall, position, limit, offset)


@router.get("/events", response_model=list[EventOut])
def get_events(
    limit: int = Query(default=100, ge=1, le=500),
    session: Session = Depends(get_session),
):
    return queries.list_events(session, limit)
