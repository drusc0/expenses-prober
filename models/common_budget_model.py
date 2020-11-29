import base64

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

        return data


class Bank:
    def __init__(self, name: str, amount: str, date: str):
        self.__name = name
        self.__amount = amount
        self.__date = date

    def name(self):
        return self.__name

    def amount(self):
        return self.__amount

    def date(self):
        return self.__date
