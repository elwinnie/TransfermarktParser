import json
from pathlib import Path

from transfermarktparser.data.match import Match


class MatchLogger:
    _SERVICE_DATA_FILE_PATH = Path('transfermarktparser/service_data/no_result_matches.json')

    _no_result_matches = []

    @property
    def no_result_matches(self):
        if not self._no_result_matches:
            self._no_result_matches = self._get_no_result_matches()
        return self._no_result_matches

    def write_unplayed(self, matches: list[Match] | Match) -> None:
        if type(matches) is not list:
            matches = [matches]

        match_logs = []
        for match in matches:
            if not match.is_result:
                match_logs.append({"league_id": match.league,
                                   "season": match.season,
                                   "home_team": match.home_team,
                                   "away_team": match.away_team, })
        if match_logs:
            uniques_match_logs = self._get_uniques_matches(match_logs)
            if uniques_match_logs:
                with open(self._SERVICE_DATA_FILE_PATH, 'w', encoding='utf-8') as ouf:
                    ouf.writelines(json.dumps(uniques_match_logs, indent=4, ensure_ascii=False))

    def _get_no_result_matches(self) -> list[dict]:
        matches = []
        try:
            with open(self._SERVICE_DATA_FILE_PATH, 'r', encoding='utf-8') as inf:
                matches = json.load(inf)
        except IOError as e:
            print(f"Could not read file with matches without result: {e}")
        except Exception as e:
            print(e)
        return matches

    def _get_uniques_matches(self, new_matches: list[dict]) -> list[dict]:
        old_matches = self.no_result_matches
        unique_matches = set()
        count = 1
        for match in [*new_matches, *old_matches]:
            count += 1
            unique_matches.add(tuple(match.items()))
        unique_matches = [dict(match) for match in unique_matches]
        return unique_matches
