from .client import Client
from google.oauth2.credentials import Credentials


class SheetsClient(Client):
    """Sheets client
    Writing the bank expenses in sheets
    """
    def ___init__(self, creds: 'Credentials', service_name: str = 'sheets', version: str = 'v4'):
        super().__init__(creds, service_name, version)
