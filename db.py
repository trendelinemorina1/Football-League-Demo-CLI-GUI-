import os
import sqlite3
from pathlib import Path
from typing import Iterable, Tuple


DB_NAME = "league.db"


def get_db_path() -> Path:
    """Return absolute path to the SQLite database file."""
    return Path(DB_NAME).resolve()


def get_connection() -> sqlite3.Connection:
    """Create a new database connection with row factory enabled."""
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """
    Initialize the database schema and seed initial data if needed.

    - Creates tables: users, matches
    - Seeds default user: lina@gmail.com / demodemo
    - Seeds a small set of Serie A matches in different states
    """
    conn = get_connection()
    cur = conn.cursor()

    # Users table (simple auth for demo purposes)
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        """
    )

    # Matches table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            home_team TEXT NOT NULL,
            away_team TEXT NOT NULL,
            kickoff_datetime TEXT NOT NULL,
            status TEXT NOT NULL, -- played, live, upcoming
            home_score INTEGER DEFAULT 0,
            away_score INTEGER DEFAULT 0
        );
        """
    )

    # Seed default user if not present
    cur.execute("SELECT COUNT(*) AS c FROM users")
    if cur.fetchone()["c"] == 0:
        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("lina@gmail.com", "demodemo"),
        )

    # Seed matches if empty
    cur.execute("SELECT COUNT(*) AS c FROM matches")
    if cur.fetchone()["c"] == 0:
        seed_matches(cur)

    conn.commit()
    conn.close()


def seed_matches(cur: sqlite3.Cursor) -> None:
    """Insert a small set of Serie A matches in various states."""
    # played
    matches: Iterable[Tuple] = [
        (
            "Inter Milan",
            "AC Milan",
            "2025-01-10 20:45",
            "played",
            2,
            1,
        ),
        (
            "Juventus",
            "Napoli",
            "2025-01-11 18:00",
            "played",
            1,
            1,
        ),
        # live
        (
            "Roma",
            "Lazio",
            "2025-01-12 21:00",
            "live",
            0,
            0,
        ),
        (
            "Atalanta",
            "Fiorentina",
            "2025-01-12 21:00",
            "live",
            1,
            0,
        ),
        # upcoming
        (
            "Udinese",
            "Bologna",
            "2025-01-20 18:30",
            "upcoming",
            0,
            0,
        ),
        (
            "Torino",
            "Genoa",
            "2025-01-21 20:45",
            "upcoming",
            0,
            0,
        ),
    ]

    cur.executemany(
        """
        INSERT INTO matches (
            home_team, away_team, kickoff_datetime,
            status, home_score, away_score
        ) VALUES (?, ?, ?, ?, ?, ?)
        """,
        matches,
    )


def ensure_db_initialized() -> None:
    """
    Ensure the database file exists and tables are created.

    Safe to call multiple times.
    """
    if not get_db_path().exists():
        init_db()
    else:
        # In case schema was never created for an existing file
        init_db()



