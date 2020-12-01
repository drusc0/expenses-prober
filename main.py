from models.common_budget_model import Email, BankExpense
from models.credentials import Credentials
from services.gmail import GmailClient
from services.datastore import DatastoreClient


def gmail_main():
    """Shows basic usage of the Gmail API.
    Uses the creds to log in and then creates a gmail client to extract
    email messages, and finally parse the data for the chase details
    """

    # If modifying these scopes, delete the file token.pickle.
    scopes = ['https://www.googleapis.com/auth/gmail.readonly']
    credentials = Credentials('token.pickle', 'credentials.json', scopes)
    cred = credentials.creds()
    # Call the Gmail API
    gmail = GmailClient(creds=cred)
    ds = DatastoreClient()

    res = gmail.get_messages()
    messages = res.get('messages', [])
    emails = []

    print(f'Emails: {len(messages)}')
    for msg in messages:
        email_id = msg.get('id', None)
        if email_id is None: continue

        email = gmail.get_message(email_id)
        # print(f'Email message: {email_id}')
        email_msg = Email(email_id, email)
        emails.append(email_msg)
        # print(f'Message: {email_msg.email_data()}')
        # print("\n---------------------------------------------\n")

    expenses = []
    for e in emails:
        data = e.email_data()
        expense = BankExpense(data)
        expenses.append(expense)
        print(f'{expense.name()} - {expense.amount()} @ {expense.date()}')

    print(f'Main: Saving to datastore...')
    ds.put_many(list(map(lambda x: x.get_properties(), expenses)))


if __name__ == '__main__':
    """Entry point to the gmail prober"""
    gmail_main()
