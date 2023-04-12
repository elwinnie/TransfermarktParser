from dataclasses import dataclass


@dataclass
class Statistics:
    match_id: int
    home_total_shots: int
    away_total_shots: int
    home_shots_off_target: int
    away_shots_off_target: int
    home_shots_saved: int
    away_shots_saved: int
    home_corners: int
    away_corners: int
    home_free_kicks: int
    away_free_kicks: int
    home_fouls: int
    away_fouls: int
    home_offsides: int
    away_offsides: int
