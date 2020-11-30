from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


class Client:
    def __init__(self, creds: 'Credentials', service_name: str, version: str):
        self.__creds = creds
        self.__service_name = service_name
        self.__version = version
        self.service = build(service_name, version, credentials=creds)

    def __str__(self):
        return f'{self.__service_name.title()}Client ver: {self.__version}'
