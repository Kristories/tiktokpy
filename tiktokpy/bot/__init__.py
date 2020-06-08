import sys
import typing
from datetime import datetime
from types import TracebackType
from typing import List

from loguru import logger

from tiktokpy.client import Client
from tiktokpy.models.trending import FeedItem, FeedItems


class TikTokPy:
    def __init__(self):
        logger.remove()
        logger.add(sys.stdout, level="DEBUG")
        logger.info("TikTokPy initialized")

    async def __aenter__(self):
        await self._init_bot()

        return self

    async def __aexit__(
        self,
        exc_type: typing.Type[BaseException] = None,
        exc_value: BaseException = None,
        traceback: TracebackType = None,
    ) -> None:
        logger.debug("Trying to close browser..")
        await self.client.browser.close()
        logger.debug("Browser successfully closed")
        logger.info("TikTokPy stopped working..")

    async def trending(self) -> List[FeedItem]:
        logger.info("Getting trending items")
        items = await self.client.trending()

        _trending = FeedItems(__root__=items)

        return _trending.__root__

    async def _init_bot(self):
        self.client: Client = await Client.create()

    @classmethod
    async def create(cls):
        self = TikTokPy()
        await self._init_bot()

        return self

    async def screenshot(self, name=None):
        if not name:
            name = datetime.now()

        await self.client.screenshot(f"screenshots/{name}.png")