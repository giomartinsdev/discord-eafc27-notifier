"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-02-14
"""
from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "leagues",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("country", sa.String(80), nullable=False),
    )
    op.create_index("ix_leagues_name", "leagues", ["name"], unique=True)
    op.create_index("ix_leagues_country", "leagues", ["country"])

    op.create_table(
        "clubs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column(
            "league_id",
            sa.Integer(),
            sa.ForeignKey("leagues.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("overall", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("attack", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("midfield", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("defense", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("budget", sa.Integer(), nullable=False, server_default="0"),
    )
    op.create_index("ix_clubs_name", "clubs", ["name"], unique=True)
    op.create_index("ix_clubs_league_overall", "clubs", ["league_id", "overall"])

    op.create_table(
        "players",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column(
            "club_id",
            sa.Integer(),
            sa.ForeignKey("clubs.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("position", sa.String(8), nullable=False),
        sa.Column("overall", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("age", sa.Integer(), nullable=False, server_default="0"),
    )
    op.create_index("ix_players_name", "players", ["name"])
    op.create_index("ix_players_position", "players", ["position"])
    op.create_index("ix_players_club_overall", "players", ["club_id", "overall"])

    op.create_table(
        "events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("type", sa.String(64), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column(
            "occurred_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_events_type", "events", ["type"])


def downgrade() -> None:
    op.drop_table("events")
    op.drop_table("players")
    op.drop_table("clubs")
    op.drop_table("leagues")
