import asyncio
import json
import google.auth

from google.cloud.pubsub import SubscriberClient
from notify import Notify
from structlog import get_logger

from app.settings import SUBSCRIPTION_ID

logger = get_logger()


async def notify(fulfilment_request):
    email_address = fulfilment_request["email_address"]
    personalisation = {"address": fulfilment_request["display_address"]}
    template_id = await get_template_id()
    Notify().send_email(email_address, template_id, personalisation)
    return True


async def get_template_id():
    return "0c5a4f95-bfa4-4364-9394-8499b4d777d5"


# pylint: disable=no-member
class PubSubConsumer:
    def __init__(self):
        self._subscriber = SubscriberClient()
        _, self.project_id = google.auth.default()
        self.subscription_path = self._subscriber.subscription_path(
            self.project_id, SUBSCRIPTION_ID
        )

    def subscribe(self, loop):
        def consume_message(message):
            PubSubConsumer.callback(message, loop)

        self._subscriber.subscribe(self.subscription_path, callback=consume_message)
        loop.run_forever()

    @staticmethod
    def callback(message, loop):
        json_message = json.loads(message.data.decode("utf-8"))
        fulfilment_request = json_message["payload"]["fulfilmentRequest"]
        asyncio.run_coroutine_threadsafe(notify(fulfilment_request), loop)
        message.ack()


def main():
    logger.info("Listening for messages...")
    loop = asyncio.get_event_loop()
    pub_sub_consumer = PubSubConsumer()
    pub_sub_consumer.subscribe(loop)
    loop.close()


if __name__ == "__main__":
    main()
