import asyncio
from asyncio import Task

import uvloop
from aiohttp import ClientSession
from fake_useragent import UserAgent
from tqdm.asyncio import tqdm
from aiohttp_retry import RetryClient, ExponentialRetry


class Request:
    def __init__(self):
        self._bed_requests: list[dict] = []
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def get(self, urls: list[str] | str, batch_number: int = 0) -> list[Task[str]]:
        if type(urls) == str:
            urls = [urls]

        headers = {'User-Agent': UserAgent().random}
        tasks = await self._make_requests(urls, headers, batch_number)
        return tasks

    async def _make_requests(self, urls: list[str], headers: dict, batch_number: int) -> list:
        tasks = []
        retry_options = ExponentialRetry(attempts=10)
        async with ClientSession(trust_env=False) as session:
            retry_client = RetryClient(raise_for_status=False, retry_options=retry_options, client_session=session,
                                       start_timeout=0.5)
            for url in urls:
                tasks.append(asyncio.create_task(self._get_page(url, headers, retry_client)))
            desc = f"Batch {batch_number}. Requests" if batch_number > 0 else "Requests"
            return await tqdm.gather(*tasks, total=len(tasks), desc=desc)

    @staticmethod
    async def _get_page(url: str, headers: dict, session: ClientSession | RetryClient) -> str | None:
        async with session.get(url, headers=headers) as response:
            html = await response.text()
        return html
