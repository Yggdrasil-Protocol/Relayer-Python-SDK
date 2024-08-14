import functools
import json
import logging
from types import NoneType
from typing import Any, Awaitable, Callable, List

import websockets

import relayer_python_sdk.config as config
import relayer_python_sdk.events as events


class RelayerWS:
    '''
    This class is used to connect to the websocket and subscribe to the feedIDs.

    Args:
        feedIDs ``(List[str])``: List of feedIDs to subscribe to.
        logger ``(logging.Logger | NoneType, optional)``: Logger to use. Defaults to None.
    '''
    def __init__(
        self, feedIDs: List[str], logger: logging.Logger | NoneType = None
    ) -> None:
        if logger is None:
            logger = logging.getLogger(__name__)
            logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )
            )
            logger.addHandler(handler)

        self.logger = logger
        self.url = config.gen_url(feedIDs)

        self.on_data_event_fn: Callable[[events.DataFeed], Awaitable[NoneType]] = (
            self._default_logger
        )
        self.on_info_event_fn: Callable[
            [events.SubscriptionMsg], Awaitable[NoneType]
        ] = self._default_logger

        self.ws = None

    async def _default_logger(self, msg: Any):
        self.logger.info("Received message: %s", msg)

    def on_data_event(
        self, func: Callable[[events.DataFeed], Awaitable[NoneType]]
    ):  # -> _Wrapped[Callable[[DataFeed], Any], Awaitable[None], Call...:
        self.on_data_event_fn = func

        @functools.wraps(func)
        async def wrapper(event: events.DataFeed) -> NoneType:
            return await func(event)

        return wrapper

    def on_info_event(
        self, func: Callable[[events.SubscriptionMsg], Awaitable[NoneType]]
    ):  # -> _Wrapped[Callable[[SubscriptionMsg], Any], Awaitable[None], Call...:
        self.on_info_event_fn = func

        @functools.wraps(func)
        async def wrapper(event: events.SubscriptionMsg) -> NoneType:
            return await func(event)

        return wrapper

    async def connect(self):
        """
        This function connects to the websocket and subscribes to the feedIDs.

        Raises:
            InvalidURI: If ``uri`` isn't a valid WebSocket URI.
            OSError: If the TCP connection fails.
            InvalidHandshake: If the opening handshake fails.
            ~asyncio.TimeoutError: If the opening handshake times out.

            ValidationError: if the event's JSON does not match their corresponding event schema.
            ValueError: if the event type is unknown.
        """
        self.logger.info(f"Subscribing to feeds")

        async with websockets.connect(
            self.url,
            logger=self.logger,
            ping_interval=config.PING_INTERVAL,
            ping_timeout=config.PING_TIMEOUT,
        ) as ws:
            self.ws = ws

            async for message in ws:
                try:
                    event = events.parse_event(str(message))
                except json.JSONDecodeError as e:
                    self.logger.error("Failed to parse event: %s", e)
                    continue

                match event:
                    case events.DataFeed():
                        await self.on_data_event_fn(event)
                    case events.SubscriptionMsg():
                        await self.on_info_event_fn(event)

    async def close(self):
        if self.ws is not None:
            await self.ws.close()
            self.ws = None
            self.logger.info("Connection closed")
        else:
            self.logger.info("Connection already closed")