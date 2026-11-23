from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_session
from app.main import app

engine = create_engine(
    "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
)
Base.metadata.create_all(engine)
TestingSession = sessionmaker(engine, expire_on_commit=False)


def override():
    with TestingSession() as session:
        yield session


app.dependency_overrides[get_session] = override
client = TestClient(app)


def test_flow():
    res = client.post("/leagues", json={"name": "Premier League", "country": "England"})
    assert res.status_code == 201, res.text
    league_id = res.json()["id"]

    assert client.post("/leagues", json={"name": "Premier League", "country": "England"}).status_code == 409

    res = client.post(
        "/clubs",
        json={
            "name": "Arsenal",
            "league_id": league_id,
            "overall": 85,
            "attack": 86,
            "midfield": 85,
            "defense": 84,
            "budget": 120_000_000,
        },
    )
    assert res.status_code == 201, res.text
    club_id = res.json()["id"]

    res = client.post(
        "/players",
        json={"name": "Saka", "club_id": club_id, "position": "RW", "overall": 86, "age": 24},
    )
    assert res.status_code == 201, res.text

    clubs = client.get(f"/clubs?league_id={league_id}&min_overall=80").json()
    assert clubs[0]["name"] == "Arsenal"
    assert client.get(f"/clubs/{club_id}").json()["name"] == "Arsenal"
    assert client.get("/clubs/9999").status_code == 404

    players = client.get(f"/players?club_id={club_id}&position=RW").json()
    assert players[0]["name"] == "Saka"

    events = client.get("/events").json()
    assert [e["type"] for e in events] == ["league.created", "club.created", "player.created"]
