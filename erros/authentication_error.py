from erros.base_error import BaseError


class AuthenticationError(BaseError):
    INVALID_CREDENTIALS = 'INVALID_CREDENTIALS'

    def __init__(self, code: str):
        message = self._get_error_message_by_code(code)

        super(AuthenticationError, self).__init__(code, message)

    @staticmethod
    def _get_error_message_by_code(code: str) -> str:
        messages = {
            'INVALID_CREDENTIALS': 'The given credentials are invalid'
        }

        return messages[code]
