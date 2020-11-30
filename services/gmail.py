from .client import Client
from typing import List

from google.oauth2.credentials import Credentials


class GmailClient(Client):
    """Gmail client
    Only useful to read data from INBOX, also, it is hardcoded with the query for chase alerts
    """
    def __init__(self, creds: 'Credentials', service_name: str = 'gmail', version: str = 'v1'):
        super().__init__(creds, service_name, version)

    def get_labels(self):
        return self.service.users()\
            .labels()\
            .list(userId='me')\
            .execute()

    def get_messages(self, q: str = None, labels: List[str] = []):
        q = q if q else "from:no.reply.alerts@chase.com"
        return self.service.users()\
            .messages()\
            .list(userId='me', includeSpamTrash=False, q=q, labelIds=labels)\
            .execute()

    def get_message(self, msg_id: str):
        return self.service.users()\
            .messages()\
            .get(userId='me', id=msg_id)\
            .execute()
