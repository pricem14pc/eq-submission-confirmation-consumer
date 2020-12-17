from asyncio import AbstractEventLoop
from typing import Coroutine

import google.auth
from google.api_core.exceptions import Unauthenticated
from google.cloud.pubsub import SubscriberClient
from google.cloud.pubsub_v1.subscriber.futures import StreamingPullFuture
from structlog import get_logger

from app.settings import SUBSCRIPTION_ID

logger = get_logger()


class Consumer:
    def __init__(self):
        credentials, self.project_id = google.auth.default()

        if not self.project_id:
            raise Unauthenticated("No authenticated project found")

        logger.debug(
            "Authenticated",
            project_id=self.project_id,
            expires=credentials.expiry.strftime("%d:%m:%YT%H:%M:%S"),
        )

        self.subscriber = SubscriberClient()
        self.subscription_path: str = self.subscriber.subscription_path(
            self.project_id, SUBSCRIPTION_ID
        )

        logger.debug(
            "Subscription path created", subscription_path=self.subscription_path
        )

    def subscribe(
        self, loop: AbstractEventLoop, callback: Coroutine
    ) -> StreamingPullFuture:
        def consume_message(message):
            callback(loop, message)

        future = self.subscriber.subscribe(
            self.subscription_path, callback=consume_message
        )
        logger.info("Listening for messages...")

        return future
