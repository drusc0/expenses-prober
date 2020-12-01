import os

from typing import List, Dict

from google.cloud import datastore


DS_CREDENTIAL_KEY = "GOOGLE_APPLICATION_CREDENTIALS"
DS_CREDENTIAL_FN = "bank-common-budget-633f71a50a38.json"

# Datastore client
# instantiates a client to push informantion extracted from gmail
# The information will be simple including only data available from email
# We do not inherit from Client due to differences in authentication
class DatastoreClient:

    KIND = 'expenses'

    def __init__(self):

        # Set the environmental variable to be able to authenticate using default
        # service account, and avoiding to pass the credentials
        if not os.environ.get(DS_CREDENTIAL_KEY):
            dir_name = os.path.dirname(os.path.abspath(__file__))
            credential_path = os.path.join(dir_name, DS_CREDENTIAL_FN)
            os.environ[DS_CREDENTIAL_KEY] = credential_path

        self.service = datastore.Client()

    # thin wrapper around put_multi call
    def put_many(self, params: List[Dict]):
        entities = []
        for entity_params in params:
            # when only providing kind, we let datastore assign an automatic id
            key = self.service.key(self.KIND)

            entity = datastore.Entity(key=key)
            for k, v in entity_params.items(): entity[k] = v

            entities.append(entity)

        print(f'Datastore: Storing entities - {entities}')
        self.service.put_multi(entities)
