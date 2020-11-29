from typing import List

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


class Client:
    def __init__(self, creds: 'Credentials', service_name: str, version: str):
        self.__creds = creds
        self.__service_name = service_name
        self.__version = version
        self.service = build(service_name, version, credentials = creds)

    def __str__(self):
        """Returns more information about the client"""
        return f'{self.__service_name.title()}Client ver: {self.__version}'


class GmailClient(Client):
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
