from typing import AsyncGenerator, Iterable

from aiohttp import ClientSession
from fake_useragent import UserAgent


class Request:
    def __init__(self):
        self._bed_requests: list[dict] = []

    async def get(self, urls: list[str] | str) -> Iterable[str]:
        if type(urls) == str:
            urls = [urls]

        headers = {'User-Agent': UserAgent().random}
        pages = self._make_requests(urls, headers)

        if self._bed_requests:
            print(self._bed_requests)

        return pages

    async def _make_requests(self, urls: list[str], headers: dict) -> Iterable[str]:
        async with ClientSession(trust_env=True) as session:
            for url in urls:
                async with session.get(url, headers=headers) as response:
                    if response.ok:
                        yield await response.text()
                    else:
                        self._bed_requests.append({'url': url, 'status': response.status})
