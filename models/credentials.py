import pickle
import os.path

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class Credentials:
    def __init__(self, token_fn: str, credentials_fn: str):
        self.__credential = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(token_fn):
            with open(token_fn, 'rb') as token:
                self.__credential = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.__credential or not self.__credential.valid:
            if self.__credential and self.__credential.expired and self.__credential.refresh_token:
                self.__credential.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_fn, SCOPES)
                self.__credential = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_fn, 'wb') as token:
                pickle.dump(self.__credential, token)

    def creds(self):
        return self.__credential
