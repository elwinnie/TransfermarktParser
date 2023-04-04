import asyncio
import collections
from dataclasses import dataclass
from typing import AsyncGenerator

import aiohttp
from aiohttp import ClientSession
from fake_useragent import UserAgent
from tqdm.asyncio import tqdm


class Request:
    def __init__(self):
        self._bed_requests: list[dict] = []

    async def get(self, urls: list[str] | str) -> AsyncGenerator[str, None]:
        if type(urls) == str:
            urls = [urls]

        headers = {'User-Agent': UserAgent().random}
        # results = asyncio.run(self._make_requests(urls, headers))

        if self._bed_requests:
            print(self._bed_requests)

        return self._make_requests(urls, headers)

    async def _make_requests(self, urls: list[str], headers: dict) -> AsyncGenerator[str, None]:
        async with ClientSession(trust_env=True) as session:
            for url in urls:
                async with session.get(url, headers=headers) as response:
                    if response.ok:
                        # data.append(await response.text())
                        yield await response.text()
                    else:
                        self._bed_requests.append({'url': url, 'status': response.status})
