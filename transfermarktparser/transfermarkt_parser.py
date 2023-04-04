import asyncio

from tqdm.asyncio import tqdm

from transfermarktparser.entities.match import Match
from transfermarktparser.parsers.schedule_parser import ScheduleParser
from transfermarktparser.utils.request import Request
from transfermarktparser.utils.url_maker import UrlMaker


class TransfermarktParser:
    @classmethod
    def get_matches(cls, league_ids: list[str], years: list[int]) -> list[Match]:
        urls = UrlMaker.get_schedule_urls(league_ids, years)
        schedule_parser = ScheduleParser()
        pages = asyncio.run(cls._parse_async(urls, schedule_parser, desc="Parse schedules"))

        return pages

    @staticmethod
    async def _parse_async(urls: list[str], parser: callable, desc=""):
        request = Request()

        pages = []
        async for html in tqdm(await request.get(urls), desc=desc, total=len(urls)):
            pages.extend(await parser.parse(html))
        return pages

    # def get_match(self, url, ):
