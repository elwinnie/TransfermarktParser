from pathlib import Path
import json


class UrlMaker:
    _SCHEDULE_URL = "https://www.transfermarkt.com/x/gesamtspielplan/wettbewerb/{league_id}/saison_id/{year}"
    _STATISTICS_URL = "https://www.transfermarkt.com/x/statistik/spielbericht/{match_id}"

    _LEAGUE_LIST_FILE = Path("league_list.json")

    def __init__(self):
        self._default_league_list = [{"league_id": "RU1", "start_year": 2013, "end_year": 2022},
                                     {"league_id": "GB1", "start_year": 2011, "end_year": 2022},
                                     {"league_id": "L1", "start_year": 2011, "end_year": 2022},
                                     {"league_id": "ES1", "start_year": 2011, "end_year": 2022},
                                     {"league_id": "FR1", "start_year": 2011, "end_year": 2022},
                                     {"league_id": "IT1", "start_year": 2011, "end_year": 2022},
                                     {"league_id": "BE1", "start_year": 2021, "end_year": 2022},
                                     {"league_id": "PO1", "start_year": 2014, "end_year": 2022},
                                     {"league_id": "NL1", "start_year": 2014, "end_year": 2022},
                                     {"league_id": "TR1", "start_year": 2011, "end_year": 2022},
                                     {"league_id": "A1", "start_year": 2011, "end_year": 2022},
                                     {"league_id": "GR1", "start_year": 2017, "end_year": 2022}, ]

    def get_statistics_url(self, match_ids: list[int]) -> list[str]:
        urls = [self._STATISTICS_URL.format(match_id=match_id) for match_id in match_ids]

        return urls

    def _get_urls(self, league_list: list[dict]) -> list[str]:
        urls = []
        for league in league_list:
            years = [year for year in range(league["start_year"], league["end_year"] + 1)]
            urls.extend([self._SCHEDULE_URL.format(league_id=league["league_id"], year=year) for year in years])
        return urls

    def _get_last_season_urls(self, league_list: list[dict]) -> list[str]:
        urls = [self._SCHEDULE_URL.format(league_id=league["league_id"], year=league["end_year"]) for league in
                league_list]
        return urls

    def get_schedule_urls(self):
        league_list = self._read_league_list()
        urls = self._get_urls(league_list)
        return urls

    def get_last_schedule_urls(self):
        league_list = self._read_league_list()
        urls = self._get_last_season_urls(league_list)
        return urls

    def _read_league_list(self):
        try:
            with open(self._LEAGUE_LIST_FILE, "r", encoding="utf-8") as ouf:
                league_list = json.loads(ouf.read())
        except OSError:
            league_list = self._default_league_list
            self._write_default_league_list()
        return league_list

    def _write_default_league_list(self):
        with open(self._LEAGUE_LIST_FILE, "w", encoding="utf-8") as ouf:
            json_file = json.dumps(self._default_league_list, indent=4, ensure_ascii=False)
            ouf.write(json_file)
