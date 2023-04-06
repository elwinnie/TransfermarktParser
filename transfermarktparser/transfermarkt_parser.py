import asyncio
from pathlib import Path

from tqdm.asyncio import tqdm

from transfermarktparser.data.match import Match
from transfermarktparser.parsers.schedule_parser import ScheduleParser
from transfermarktparser.utils.match_logger import MatchLogger
from transfermarktparser.utils.request import Request
from transfermarktparser.utils.url_maker import UrlMaker


class TransfermarktParser:
    _SERVICE_DATA = Path('transfermarktparser/service_data')

    def __init__(self, track_future_matches: bool = True):
        self._track_future_matches = track_future_matches
        self._schedule_parser = ScheduleParser()
        self._match_logger = MatchLogger()

    def get_all_matches(self, league_ids: list[str], years: list[int]) -> list[Match]:
        urls = UrlMaker.get_schedule_urls(league_ids, years)
        matches = asyncio.run(self._parse_async(urls, self._schedule_parser.parse_matches, desc="Parse schedules"))

        self._match_logger.write_unplayed(matches)

        return matches

    def get_match(self, league_id: str, year: int, home_team: str, away_team: str) -> Match:
        url = UrlMaker.get_schedule_urls(league_id, year)
        match = asyncio.run(self._parse_async(url, self._schedule_parser.parse_matches, desc="Match_parse",
                                              searched_matches=[{"home_team": home_team, "away_team": away_team}]))

        self._match_logger.write_unplayed(match)
        return match[0]

    @staticmethod
    async def _parse_async(urls: list[str], parser: callable, desc="", **params):
        request = Request()
        pages = []
        async for html in tqdm(await request.get(urls), desc=desc, total=len(urls)):
            if params:
                pages.extend(parser(page=html, **params))
            else:
                pages.extend(parser(page=html))
        return pages
