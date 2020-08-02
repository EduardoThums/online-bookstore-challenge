from errors.base_error import BaseError


class BusinessError(BaseError):
    BOOK_NOT_FOUND = 'BOOK_NOT_FOUND'
    NOT_ALLOWED_TO_BORROW_OWN_BOOK = 'NOT_ALLOWED_TO_BORROW_OWN_BOOK'
    BOOK_CANT_BE_BORROWED = 'BOOK_CANT_BE_BORROWED'
    USER_NOT_FOUND = 'USER_NOT_FOUND'
    INVALID_EMAIL_FORMAT = 'INVALID_EMAIL_FORMAT'
    INVALID_PASSWORD_FORMAT = 'INVALID_PASSWORD_FORMAT'
    USER_ALREADY_REGISTERED = 'USER_ALREADY_REGISTERED'
    BOOK_BORROWING_NOT_FOUND = 'BOOK_BORROWING_NOT_FOUND'
    NOT_ALLOWED_TO_RETURN_BOOK_WITH_OPEN_FINE = 'NOT_ALLOWED_TO_RETURN_BOOK_WITH_OPEN_FINE'
    BOOK_DOESNT_BELONG_TO_USER = 'BOOK_DOESNT_BELONG_TO_USER'

    def __init__(self, code: str):
        message = self._get_error_message_by_code(code)

        super(BusinessError, self).__init__(code, message)

    @staticmethod
    def _get_error_message_by_code(code: str) -> str:
        messages = {
            'BOOK_NOT_FOUND': 'Book does not exist',
            'NOT_ALLOWED_TO_BORROW_OWN_BOOK': 'Its not allowed to borrow your own book',
            'BOOK_CANT_BE_BORROWED': 'The book cant be borrowed due his status',
            'USER_NOT_FOUND': 'User does not exist',
            'INVALID_EMAIL_FORMAT': 'The email format is not valid',
            'INVALID_PASSWORD_FORMAT': 'The password format is not valid',
            'USER_ALREADY_REGISTERED': 'An user is already registered with this email',
            'BOOK_BORROWING_NOT_FOUND': 'The book it\'s borrowing doest no exist',
            'NOT_ALLOWED_TO_RETURN_BOOK_WITH_OPEN_FINE': 'Its not allowed to return book with open fine',
            'BOOK_DOESNT_BELONG_TO_USER': 'The book doesnt belongs to you'
        }

        return messages[code]
