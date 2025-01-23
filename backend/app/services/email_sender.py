from abc import ABC, abstractmethod
import os
import logging

import boto3
from botocore.exceptions import ClientError, BotoCoreError

logger = logging.getLogger(__name__)


class BaseEmailSender(ABC):
    """
    Responsible for sending emails via Amazon SES.
    """

    @staticmethod
    def create_email_sender() -> "BaseEmailSender":
        """
        Tries to log into AWS.
        If credentials are present, logs in and returns an EmailSender.
        If no credentials are found, returns a FakeEmailSender.
        """

        try:
            sts = boto3.client("sts")
            identity = sts.get_caller_identity()
            logger.info(f"Logged into AWS with user {identity['Arn']}.")
            return EmailSender()

        except (BotoCoreError, ClientError) as exc:
            logger.warning(
                f"Invalid AWS credentials, using a fake email sender. {exc=}"
            )

        return FakeEmailSender()

    @abstractmethod
    def send_email(subject: str, body: str) -> None:
        """
        Send an email.
        :param subject: Email subject.
        :param body: Email body.
        """


class FakeEmailSender(BaseEmailSender):
    """
    Fake email sender, just logs imaginary emails.
    """

    def send_email(self, subject, body):
        logger.info(f"Sending fake email '{subject}':\n{body}")


class EmailSender(BaseEmailSender):
    """
    Real email sender, uses Amazon SES (Simple Email Service) to send emails to the EMAIL_RECIPIENT (environment variable).
    """

    def __init__(self):
        super().__init__()
        self.ses_client = boto3.client("ses")
        self.sender = os.environ["EMAIL_SENDER"]
        self.recipient = os.environ["EMAIL_RECIPIENT"]

    def send_email(self, subject, body):
        logger.info(f"Sending email '{subject}' to '{self.recipient}':\n{body}")

        response = self.ses_client.send_email(
            Source=self.sender,
            Destination={
                "ToAddresses": [
                    self.recipient,
                ]
            },
            Message={
                "Subject": {"Data": subject},
                "Body": {"Text": {"Data": body}},
            },
        )

        logger.info(f"Successfully sent email with MessageId {response['MessageId']}")
