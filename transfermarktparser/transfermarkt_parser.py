import asyncio
import concurrent.futures
from asyncio import Task
from datetime import datetime

from tqdm import tqdm

from transfermarktparser.parsers.schedule_parser import ScheduleParser
from transfermarktparser.parsers.statistics_parser import StatisticsParser
from transfermarktparser.utils.data_exporter import DataExporter
from transfermarktparser.utils.match_checker import MatchChecker
from transfermarktparser.utils.request import Request
from transfermarktparser.utils.url_maker import UrlMaker


class TransfermarktParser:
    def __init__(self, max_workers: int = None):
        self._max_workers = max_workers
        self._schedule_parser = ScheduleParser()
        self._statistics_parser = StatisticsParser()
        self._match_logger = MatchChecker()
        self._exporter = DataExporter()
        self._url_maker = UrlMaker()

        self._matches = []

    def get(self, use_timestamp: bool = True, update_only: bool = False):
        timestamp = self._get_timestamp() if use_timestamp else None

        if update_only:
            urls = self._url_maker.get_last_schedule_urls()
        else:
            urls = self._url_maker.get_schedule_urls()
        self._get_schedules(urls, timestamp=timestamp, check_new_matches=update_only)

        if self._matches:
            urls = self._url_maker.get_statistics_url([match.match_id for match in self._matches])
            self._get_statistics(urls, timestamp)

    def _get_schedules(self, urls: list[str], check_new_matches: bool, timestamp: str = None):
        self._matches.clear()
        print(f"Start parsing {len(urls)} pages of schedules...")
        self._matches, *_ = self._parse(urls, self._schedule_parser.parse, desc="Parse schedules")
        self._matches = self._match_logger.find_new_matches(self._matches, check_new_matches=check_new_matches)
        if self._matches:
            self._exporter.to_csv(self._matches, "schedule", timestamp=timestamp)

    def _get_statistics(self, urls: list[str], timestamp: str = None):
        print(f"\nStart parsing {len(urls)} pages of statistics...")
        parsed_pages = 0
        for statistics in self._parse(urls, self._statistics_parser.parse, desc="Parse statistics"):
            parsed_pages += len(statistics)
            if parsed_pages:
                self._exporter.to_csv(statistics, "statistics", mode="a", timestamp=timestamp)
        print(f"{parsed_pages}/{len(urls)} were parsed statistics pages.")

    def _parse(self, urls: list[str], parser: callable, desc: str | None) -> list:
        request = Request()
        batch_number = 1
        for batch_urls in self._divide_batches(urls):
            htmls = asyncio.run(request.get(batch_urls, batch_number=batch_number))
            pages = self._multiprocessor_parse(htmls, parser, desc)
            batch_number += 1
            # sleep(random.randint(1, 10))

            yield pages

    def _multiprocessor_parse(self, htmls: list[Task[str]], parser: callable, desc: str | None):
        pages = []
        with concurrent.futures.ProcessPoolExecutor(max_workers=self._max_workers) as executor:
            for page in tqdm(executor.map(parser, htmls), total=len(htmls), desc=desc):
                if page:
                    if type(page) == list:
                        pages.extend(page)
                    else:
                        pages.append(page)
        return pages

    @staticmethod
    def _divide_batches(data: list, size=5000) -> list:
        for i in range(0, len(data), size):
            yield data[i: i + size]

    @staticmethod
    def _get_timestamp() -> str:
        timestamp = datetime.now()
        return timestamp.strftime('%d_%m_%Y_%H_%M')
