from unittest import TestCase
from unittest.mock import MagicMock, patch

from domain.book.entities.book_entity import Book, BookStatus
from domain.book.use_cases.register_book.register_book_use_case import RegisterBookUseCase
from errors.business_error import BusinessError

module_path = RegisterBookUseCase.__module__


class TestRegisterBookUseCase(TestCase):

    def test_register_book_should_succeed(self):
        flask_request = MagicMock(
            logged_user=MagicMock(user_id='5f260aadcbd8d651ca92dd7f')
        )

        with patch(f'{module_path}.request', flask_request), \
                patch.object(Book, 'first', return_value=None), \
                patch.object(Book, 'save', spec=True) as save_book:
            use_case = RegisterBookUseCase(
                title='title',
                description='description',
                author='author'
            )
            use_case.exec()

            save_book.assert_called_once()

            self.assertEqual('title', use_case.registered_book.title)
            self.assertEqual('description', use_case.registered_book.description)
            self.assertEqual('author', use_case.registered_book.author)
            self.assertEqual(BookStatus.AVAILABLE.value, use_case.registered_book.status)

    def test_register_book_given_already_used_title_should_raise_error(self):
        flask_request = MagicMock(
            logged_user=MagicMock(user_id='5f260aadcbd8d651ca92dd7f')
        )

        with patch(f'{module_path}.request', flask_request), \
                patch.object(Book, 'first', return_value=Book()):
            try:
                RegisterBookUseCase(
                    title='title',
                    description='description',
                    author='author'
                ).exec()

                self.fail()
            except BusinessError as e:
                self.assertEqual(BusinessError.BOOK_ALREADY_REGISTERED, e.code)
