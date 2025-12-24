import random
from datetime import datetime
from typing import List, Optional

from .db import get_connection, ensure_db_initialized
from .models import Match, MatchStatus, User


class AuthService:
    """Very simple authentication service using plain-text passwords."""

    def __init__(self) -> None:
        ensure_db_initialized()

    def authenticate(self, username: str, password: str) -> Optional[User]:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, username FROM users WHERE username = ? AND password = ?",
            (username, password),
        )
        row = cur.fetchone()
        conn.close()
        if row is None:
            return None
        return User(id=row["id"], username=row["username"])


class LeagueService:
    """Business logic for working with matches."""

    def __init__(self) -> None:
        ensure_db_initialized()

    def _row_to_match(self, row) -> Match:
        return Match(
            id=row["id"],
            home_team=row["home_team"],
            away_team=row["away_team"],
            kickoff_datetime=datetime.strptime(
                row["kickoff_datetime"], "%Y-%m-%d %H:%M"
            ),
            status=row["status"],  # type: ignore[assignment]
            home_score=row["home_score"],
            away_score=row["away_score"],
        )

    def get_matches(self, status: Optional[MatchStatus] = None) -> List[Match]:
        conn = get_connection()
        cur = conn.cursor()
        if status:
            cur.execute(
                "SELECT * FROM matches WHERE status = ? ORDER BY kickoff_datetime",
                (status,),
            )
        else:
            cur.execute("SELECT * FROM matches ORDER BY kickoff_datetime")
        rows = cur.fetchall()
        conn.close()
        return [self._row_to_match(r) for r in rows]

    def simulate_live_updates(self) -> None:
        """
        Randomly update scores for live matches.

        This function is idempotent and fast; safe to call periodically
        from CLI or GUI to simulate in-progress matches.
        """
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM matches WHERE status = 'live'")
        live_rows = cur.fetchall()
        if not live_rows:
            conn.close()
            return

        for row in live_rows:
            # 40% chance that a goal happens in this "tick"
            if random.random() < 0.4:
                home_score = row["home_score"]
                away_score = row["away_score"]
                # Randomly pick which team scores
                if random.random() < 0.5:
                    home_score += 1
                else:
                    away_score += 1
                cur.execute(
                    """
                    UPDATE matches
                    SET home_score = ?, away_score = ?
                    WHERE id = ?
                    """,
                    (home_score, away_score, row["id"]),
                )

        conn.commit()
        conn.close()


