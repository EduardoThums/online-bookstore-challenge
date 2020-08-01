import re

from domain.base.use_cases.base_use_case import BaseUseCase
from domain.user.entities.user_entity import User
from errors.business_error import BusinessError
from helpers.crypto.crypto_helper import CryptoHelper

_VALID_EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
_CONTAINS_NUMBER_REGEX = r"\d"
_CONTAINS_UPPER_AND_LETTER_CASES = r"^(?=[A-Z]*[a-z])(?=[a-z]*[A-Z])"


class RegisterUserUseCase(BaseUseCase):

    def __init__(self, email: str, password: str, name: str):
        self.email = email
        self.password = password
        self.name = name

    def exec(self):
        self._check_if_email_is_valid()

        self._check_if_password_is_valid()

        self._check_if_email_is_already_registered()

        hashed_password = CryptoHelper.hash_password(self.password)

        new_user = User(
            email=self.email,
            name=self.name,
            password=hashed_password
        )

        new_user.save()

    def _check_if_email_is_valid(self):
        if not re.fullmatch(_VALID_EMAIL_REGEX, self.email):
            raise BusinessError(code=BusinessError.INVALID_EMAIL_FORMAT)

    def _check_if_password_is_valid(self):
        has_at_least_eight_characters = len(self.password) >= 8
        has_at_least_one_number = re.findall(_CONTAINS_NUMBER_REGEX, self.password)
        has_at_least_one_upper_and_lower_case = re.findall(_CONTAINS_UPPER_AND_LETTER_CASES, self.password)

        if not has_at_least_eight_characters or \
                not has_at_least_one_number or \
                not has_at_least_one_upper_and_lower_case:
            raise BusinessError(code=BusinessError.INVALID_PASSWORD_FORMAT)

    def _check_if_email_is_already_registered(self):
        registered_user = User.objects(email=self.email)

        if registered_user:
            raise BusinessError(code=BusinessError.USER_ALREADY_REGISTERED)
