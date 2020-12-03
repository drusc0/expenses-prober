import base64
import re
import pytz

from datetime import datetime
from pytz import timezone
from typing import Dict


class Email:
    """Email class object to hold import email message information
    We can parse the message payloade and decode the data
    """

    def __init__(self, email_id: str, message: Dict):
        self.__email_id = email_id
        self.__message = message

    def __str__(self):
        return f'Email: {self.__email_id}'

    def email_data(self):
        _payload = self.__message.get('payload', {})
        _body = _payload.get('body', {})
        _data = _body.get('data', None)
        try:
            data = base64.b64decode(_data)
            return data.decode('utf-8')
        except Exception as err:
            print(f"Error: {err}. Email data - {_data}")
            return ""


class BankExpense:
    """BankExpense class object to hold the bank expenses
    Three important details for this class is the amount, location where it was charged, and date
    There is no other important data in the push email sent from Chase, it can change if adding
    other bank's alrts
    """
    def __init__(self, data: str):
        self.__data = data
        self.__parsed_data = None
        self.__pattern = re.compile(r'A charge of \(\$USD\) ([\d+\.]+) at '
                                    r'([\s\S]+) has been authorized on ([\S, ]+) at', re.IGNORECASE)

    def __str__(self):
        return f'Bank expense: {self.__parsed_data}'

    def _get_parsed_message(self):
        if self.__parsed_data is None:
            self.__parsed_data = self.__pattern.search(self.__data)

        return self.__parsed_data

    def name(self):
        _res = self._get_parsed_message()
        return _res.group(2)

    def amount(self):
        _res = self._get_parsed_message()
        return _res.group(1)

    def date(self):
        _res = self._get_parsed_message()
        _date_str = _res.group(3)
        _date = datetime.strptime(_date_str, '%b %d, %Y')
        _date = _date.astimezone(timezone('US/Pacific'))
        return _date

    def get_properties(self):
        return {
            'expense_location': self.name(),
            'amount': float(self.amount()),
            'expense_date': self.date()
        }