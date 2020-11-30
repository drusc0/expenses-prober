import base64
import re

from datetime import datetime
from typing import Dict


class Email:
    def __init__(self, email_id: str, message: Dict):
        self.__email_id = email_id
        self.__message = message

    def __str__(self):
        return f'Email: {self.__email_id}'

    def email_data(self):
        _payload = self.__message.get('payload', {})
        _body = _payload.get('body', {})
        _data = _body.get('data', None)
        data = base64.b64decode(_data) if _data else ""

        return data.decode('utf-8')


class BankExpense:
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
        return _date
