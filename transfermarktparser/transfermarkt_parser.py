import asyncio

from transfermarktparser.parsers.schedule_parser import ScheduleParser
from transfermarktparser.utils.request import Request


class TransfermarktParser:
    @staticmethod
    def get_matches(league_ids: list[str], years: list[int]):
        urls =
        request = Request()
        htmls = request.get(urls)
        schedule_parser = ScheduleParser()

        pages = []
        for html in htmls:
            pages.extend(schedule_parser.parse(html))

        return pages

    def get_match(self, url, ):
