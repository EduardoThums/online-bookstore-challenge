from unittest import TestCase
from unittest.mock import patch, MagicMock

from bson import ObjectId

from domain.book.entities.book_entity import Book, BookStatus
from domain.book.use_cases.borrow_book.borrow_book_use_case import BorrowBookUseCase
from domain.book_borrowing.entities.book_borrowing_entity import BookBorrowing
from domain.user.entities.user_entity import User
from errors.business_error import BusinessError

module_path = BorrowBookUseCase.__module__


class TestBorrowBookUseCase(TestCase):

    def test_borrow_book_should_succeed(self):
        book = Book(
            user=User(id='5f25f58f3d9eb32fd95f149d')
        )

        flask_request = MagicMock(
            logged_user=MagicMock(user_id=ObjectId('5f25f5963d9eb32fd95f149e'))
        )

        with patch.object(Book, 'first', return_value=book), \
                patch(f'{module_path}.request', flask_request), \
                patch.object(Book, 'save', spec=True) as save_book, \
                patch.object(BookBorrowing, 'save', spec=True) as save_book_borrowing:
            BorrowBookUseCase(
                book_id='5f2605836cf256086fc8be0b'
            ).exec()

            book.status = BookStatus.BORROWED.value
            save_book.assert_called_once()

            save_book_borrowing.assert_called_once()

    def test_borrow_book_that_doesnt_exist_should_raise_error(self):
        try:
            BorrowBookUseCase(
                book_id='5f2605836cf256086fc8be0b'
            ).exec()

            self.fail()
        except BusinessError as e:
            self.assertEqual(BusinessError.BOOK_NOT_FOUND, e.code)

    def test_borrow_book_that_you_own_should_raise_error(self):
        book = Book(
            user=User(id='5f25f58f3d9eb32fd95f149d')
        )

        flask_request = MagicMock(
            logged_user=MagicMock(user_id=ObjectId('5f25f58f3d9eb32fd95f149d'))
        )

        with patch.object(Book, 'first', return_value=book), \
                patch(f'{module_path}.request', flask_request):
            try:
                BorrowBookUseCase(
                    book_id='5f2605836cf256086fc8be0b'
                ).exec()

                self.fail()
            except BusinessError as e:
                self.assertEqual(BusinessError.NOT_ALLOWED_TO_BORROW_OWN_BOOK, e.code)

    def test_borrow_book_that_is_already_borrowed_should_raise_error(self):
        book = Book(
            user=User(id='5f25f58f3d9eb32fd95f149d'),
            status=BookStatus.BORROWED.value
        )

        flask_request = MagicMock(
            logged_user=MagicMock(user_id=ObjectId('5f25f5963d9eb32fd95f149e'))
        )

        with patch.object(Book, 'first', return_value=book), \
                patch(f'{module_path}.request', flask_request):
            try:
                BorrowBookUseCase(
                    book_id='5f2605836cf256086fc8be0b'
                ).exec()

                self.fail()
            except BusinessError as e:
                self.assertEqual(BusinessError.BOOK_CANT_BE_BORROWED, e.code)
