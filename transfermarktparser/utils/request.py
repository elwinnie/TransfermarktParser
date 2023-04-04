import asyncio
from dataclasses import dataclass

import aiohttp
from aiohttp import ClientSession
from fake_useragent import UserAgent
from tqdm.asyncio import tqdm


class Request:
    def __init__(self):
        self._bed_requests: list[dict] = []

    def get(self, urls: list[str] | str) -> dict:
        if type(urls) == str:
            urls = [urls]

        headers = {'User-Agent': UserAgent().random}
        results = asyncio.run(self._make_requests(urls, headers))

        if self._bed_requests:
            print(self._bed_requests)

        return results

    async def _make_requests(self, urls: list[str], headers: dict) -> list[str]:
        data = []
        async with ClientSession(trust_env=True) as session:
            async for url in tqdm(urls):
                async with session.get(url, headers=headers) as response:
                    if response.ok:
                        data.append(await response.text())
                    else:
                        self._bed_requests.append({'url': url, 'status': response.status})
        return data
