# Author: Oskar Domingos
# This class contains models that structures how data will be stored in application

from Shared.models import User


# Request is either a review or query
class Request:
    def __init__(self, request_id, request_type, user_id, username, content):
        print(f'Request created. Request type: {request_type}, username: {username}, content: {content}')
        self._request_id = request_id
        self._request_type = request_type
        self._author = User(username=username, user_id=user_id)
        self._content = content

    def __repr__(self):
        return f'{self._request_id} {self._request_type}'

    @property
    def request_id(self):
        return self._request_id

    @property
    def request_type(self):
        return self._request_type

    @property
    def author(self):
        return self._author

    @property
    def content(self):
        return self._content
