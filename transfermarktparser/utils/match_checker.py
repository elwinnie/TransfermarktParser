from pathlib import Path

from transfermarktparser.data.match import Match


class MatchChecker:
    _SERVICE_DATA_FILE_PATH = Path('transfermarktparser/service_data/future_games.txt')

    def find_new_matches(self, matches: list[Match], check_new_matches: bool = True) -> list[Match]:
        new_matches = []
        new_futures_matches = []

        future_matches = self._get_future_matches()
        for match in matches:
            if check_new_matches and future_matches:
                if match.is_result and match.match_id in future_matches:
                    new_matches.append(match)
                elif not match.is_result:
                    new_futures_matches.append(match.match_id)
            else:
                if match.is_result:
                    new_matches.append(match)
                else:
                    new_futures_matches.append(match.match_id)

        self._write_future_matches(new_futures_matches)
        return new_matches

    def _get_future_matches(self) -> list[dict]:
        match_ids = []
        try:
            with open(self._SERVICE_DATA_FILE_PATH, 'r', encoding='utf-8') as inf:
                match_ids = list(map(int, inf.read().split()))
        except OSError:
            pass

        return match_ids

    def _write_future_matches(self, future_matches) -> None:
        with open(self._SERVICE_DATA_FILE_PATH, "w", encoding='utf-8') as ouf:
            for match in future_matches:
                ouf.write(f"{match} ")
