from unittest import TestCase
from unittest.mock import patch

from domain.user.entities.user_entity import User
from domain.user.use_cases.register_user.register_user_use_case import RegisterUserUseCase
from errors.business_error import BusinessError


class TestRegisterUserUseCase(TestCase):

    def test_register_user_should_succeed(self):
        with patch.object(User, 'objects', return_value=None), \
                patch.object(User, 'save', spec=True) as save_user:
            RegisterUserUseCase(
                email='user@mail.com',
                password='Test123*',
                name='name'
            ).exec()

            save_user.assert_called_once()

    def test_register_with_invalid_email_should_raise_error(self):
        try:
            RegisterUserUseCase(
                email='mail.com',
                password='Test123*',
                name='name'
            ).exec()

            self.fail()
        except BusinessError as e:
            self.assertEqual(BusinessError.INVALID_EMAIL_FORMAT, e.code)

    def test_register_with_password_without_at_least_eight_characters_should_raise_error(self):
        try:
            RegisterUserUseCase(
                email='user@mail.com',
                password='Aa123',
                name='name'
            ).exec()

            self.fail()
        except BusinessError as e:
            self.assertEqual(BusinessError.INVALID_PASSWORD_FORMAT, e.code)

    def test_register_with_password_without_at_least_one_number_should_raise_error(self):
        try:
            RegisterUserUseCase(
                email='user@mail.com',
                password='aAaAaAaA',
                name='name'
            ).exec()

            self.fail()
        except BusinessError as e:
            self.assertEqual(BusinessError.INVALID_PASSWORD_FORMAT, e.code)

    def test_register_with_password_without_at_least_one_upper_and_lower_case_should_raise_error(self):
        try:
            RegisterUserUseCase(
                email='user@mail.com',
                password='12345678',
                name='name'
            ).exec()

            self.fail()
        except BusinessError as e:
            self.assertEqual(BusinessError.INVALID_PASSWORD_FORMAT, e.code)

    def test_register_with_already_used_email_should_raise_error(self):
        user_with_same_email = User(email='user@mail.com')

        with patch.object(User, 'objects', return_value=user_with_same_email):
            try:
                RegisterUserUseCase(
                    email='user@mail.com',
                    password='Test123*',
                    name='name'
                ).exec()

                self.fail()
            except BusinessError as e:
                self.assertEqual(BusinessError.USER_ALREADY_REGISTERED, e.code)
