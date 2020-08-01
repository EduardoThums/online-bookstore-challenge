import functools

from flask import request

from domain.user.entities.user_entity import User
from errors.authentication_error import AuthenticationError
from helpers.database.database_helper import DatabaseHelper
from helpers.jwt.jwt_helper import JwtHelper


class LoggedUserModel:

    def __init__(self, user_payload: dict):
        self.user_id = DatabaseHelper.convert_to_object_id(user_payload['user_id'])
        self.user_email = user_payload['user_email']
        self.user_name = user_payload['user_name']


def require_logged_user(func):

    @functools.wraps(func)
    def func_wrapper(*args, **kwargs):
        access_token = request.headers['Authorization']
        token_payload = JwtHelper.decode_token(access_token)

        if not token_payload:
            raise AuthenticationError(code=AuthenticationError.INVALID_CREDENTIALS)

        user_email = token_payload['user_email']

        registered_user = User.objects(email=user_email)

        if registered_user:
            request.logged_user = LoggedUserModel(user_payload=token_payload)

            return func(*args, **kwargs)
        else:
            raise AuthenticationError(code=AuthenticationError.INVALID_CREDENTIALS)

    return func_wrapper
