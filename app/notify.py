from notifications_python_client import NotificationsAPIClient
from structlog import get_logger

from app.settings import NOTIFY_API_KEY

logger = get_logger()


class Notify:
    def __init__(self):
        self.notifications_client = NotificationsAPIClient(NOTIFY_API_KEY)

    def send_email(self, email_address, template_id, personalisation):
        logger.info("sending message ...")
        self.notifications_client.send_email_notification(
            email_address=email_address,
            template_id=template_id,
            personalisation=personalisation,
        )

