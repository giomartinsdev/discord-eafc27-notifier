from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class LeagueIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    country: str = Field(min_length=1, max_length=80)


class LeagueOut(LeagueIn):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ClubIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    league_id: int
    overall: int = Field(default=0, ge=0, le=99)
    attack: int = Field(default=0, ge=0, le=99)
    midfield: int = Field(default=0, ge=0, le=99)
    defense: int = Field(default=0, ge=0, le=99)
    budget: int = Field(default=0, ge=0)


class ClubOut(ClubIn):
    id: int
    model_config = ConfigDict(from_attributes=True)


class PlayerIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    club_id: int
    position: str = Field(min_length=1, max_length=8)
    overall: int = Field(default=0, ge=0, le=99)
    age: int = Field(default=0, ge=15, le=60)


class PlayerOut(PlayerIn):
    id: int
    model_config = ConfigDict(from_attributes=True)


class EventOut(BaseModel):
    id: int
    type: str
    payload: dict
    occurred_at: datetime
    model_config = ConfigDict(from_attributes=True)
