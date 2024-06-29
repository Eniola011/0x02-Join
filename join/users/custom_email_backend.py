from django.core.mail.backends.base import BaseEmailBackend
from .gmail import send_email  # Import your custom send_email function

class GmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        for message in email_messages:
            send_email(
                to=message.to[0],
                subject=message.subject,
                body=message.body
            )
        return len(email_messages)
