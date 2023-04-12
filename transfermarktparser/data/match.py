import datetime
from dataclasses import dataclass


@dataclass
class Match:
    league: str
    country: str
    level: int
    season: int

    date: datetime.date
    time: datetime.time
    tour: int

    home_team: str
    home_score: int | None

    away_team: str
    away_score: int | None

    home_id: int
    away_id: int
    match_id: int
    league_id: str

    @property
    def is_result(self):
        if self.home_score is None and self.away_score is None:
            return False
        return True
