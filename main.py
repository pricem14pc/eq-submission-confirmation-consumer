#!/usr/bin/env python
import asyncio
from asyncio.events import AbstractEventLoop

import orjson as json
import uvloop
from google.cloud.pubsub_v1.subscriber.message import Message
from structlog import get_logger

from app import Consumer, Notifier

logger = get_logger()


def notify(fulfilment_request) -> bool:
    email_address = fulfilment_request["email_address"]
    personalisation = {"address": fulfilment_request["display_address"]}
    template_id = "0c5a4f95-bfa4-4364-9394-8499b4d777d5"

    Notifier().send_email(email_address, template_id, personalisation)
    return True


def callback(loop: AbstractEventLoop, message: Message) -> None:
    logger.debug("Processing message", data=message.data)
    data = json.loads(message.data)

    fulfilment_request = data["payload"]["fulfilmentRequest"]
    loop.run_in_executor(None, notify, fulfilment_request)

    logger.debug("Acknowledging message", ack_id=message.ack_id)
    message.ack()


def main() -> None:
    """Run a GCP PubSub subscriber that forwards messages to Gov Notify."""
    loop = asyncio.get_event_loop()

    consumer = Consumer()

    logger.info("Running asynchronous subscriber")
    consumer.subscribe(loop, callback)

    loop.run_forever()


if __name__ == "__main__":
    uvloop.install()
    main()
