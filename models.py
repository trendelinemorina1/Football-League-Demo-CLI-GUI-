from dataclasses import dataclass
from datetime import datetime
from typing import Literal


MatchStatus = Literal["played", "live", "upcoming"]


@dataclass
class User:
    id: int
    username: str


@dataclass
class Match:
    id: int
    home_team: str
    away_team: str
    kickoff_datetime: datetime
    status: MatchStatus
    home_score: int
    away_score: int

    @property
    def date_str(self) -> str:
        return self.kickoff_datetime.strftime("%Y-%m-%d")

    @property
    def time_str(self) -> str:
        return self.kickoff_datetime.strftime("%H:%M")

    @property
    def score_str(self) -> str:
        if self.status in ("played", "live"):
            return f"{self.home_score} - {self.away_score}"
        return "-"


