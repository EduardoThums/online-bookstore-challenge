from unittest import TestCase
from unittest.mock import patch

from domain.user.entities.user_entity import User
from domain.user.use_cases.login.login_use_case import LoginUseCase
from errors.authentication_error import AuthenticationError
from errors.business_error import BusinessError
from helpers.crypto.crypto_helper import CryptoHelper
from helpers.jwt.jwt_helper import JwtHelper


class TestLoginUseCase(TestCase):

    def test_login_should_login(self):
        user = User(
            password='hashed_password'
        )

        access_token = 'access_token'

        with patch.object(User, 'first', return_value=user), \
                patch.object(CryptoHelper, 'check_password', return_value=True),  \
                patch.object(JwtHelper, 'encode_token', return_value=access_token):
            use_case = LoginUseCase(
                email='user@mail.com',
                password='Test123*'
            )
            use_case.exec()

            self.assertEqual('access_token', use_case.access_token)

    def test_login_with_non_existent_user_should_raise_error(self):
        try:
            LoginUseCase(
                email='user@mail.com',
                password='Test123*'
            ).exec()

            self.fail()
        except BusinessError as e:
            self.assertEqual(BusinessError.USER_NOT_FOUND, e.code)

    def test_login_given_password_that_doesnt_match_should_raise_error(self):
        user = User(
            password='hashed_password'
        )

        with patch.object(User, 'first', return_value=user), \
                patch.object(CryptoHelper, 'check_password', return_value=False):
            try:
                LoginUseCase(
                    email='user@mail.com',
                    password='Test123*'
                ).exec()

                self.fail()
            except AuthenticationError as e:
                self.assertEqual(AuthenticationError.INVALID_CREDENTIALS, e.code)
