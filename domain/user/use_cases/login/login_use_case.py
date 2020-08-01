from domain.base.use_cases.base_use_case import BaseUseCase
from domain.user.entities.user_entity import User
from erros.authentication_error import AuthenticationError
from erros.business_error import BusinessError
from helpers.crypto.crypto_helper import CryptoHelper
from helpers.jwt.jwt_helper import JwtHelper


class LoginUseCase(BaseUseCase):

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

        self.access_token = None

    def exec(self):
        registered_user = User.first(email=self.email)

        if not registered_user:
            raise BusinessError(code=BusinessError.USER_NOT_FOUND)

        self._check_if_passwords_are_equal(hashed_password=registered_user.password)

        self.access_token = JwtHelper.encode_token(
            user_id=str(registered_user.id),
            user_email=self.email,
            user_name=registered_user.name
        )

    def _check_if_passwords_are_equal(self, hashed_password: str):
        are_the_passwords_equal = CryptoHelper.check_password(
            password=self.password,
            hashed_password=hashed_password
        )

        if not are_the_passwords_equal:
            raise AuthenticationError(code=AuthenticationError.INVALID_CREDENTIALS)
