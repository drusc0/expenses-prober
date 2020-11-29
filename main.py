from models.common_budget_model import Email
from models.credentials import Credentials
from services.services import GmailClient


def main():
    """Shows basic usage of the Gmail API.
    Uses the creds to log in and then creates a gmail client to extract
    email messages, and finally parse the data for the chase details
    """
    credentials = Credentials('token.pickle', 'credentials.json')
    cred = credentials.creds()
    # Call the Gmail API
    gmail = GmailClient(creds=cred)

    res = gmail.get_messages()
    messages = res.get('messages', [])

    print(f'Emails: {len(messages)}')
    for msg in messages:
        email_id = msg.get('id', None)
        if email_id is None: continue

        email = gmail.get_message(email_id)
        print(f'Email message: {email_id}')
        email_msg = Email(email_id, email)
        print(f'Message: {email_msg.email_data()}')
        print("\n---------------------------------------------\n")


if __name__ == '__main__':
    """Entry point to the gmail prober"""
    main()
