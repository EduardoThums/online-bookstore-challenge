from unittest import TestCase
from unittest.mock import patch, MagicMock

from bson import ObjectId

from domain.book.entities.book_entity import Book, BookStatus
from domain.book.use_cases.remove_book_fine.remove_book_fine_use_case import RemoveBookFineUseCase
from domain.book_borrowing.entities.book_borrowing_entity import BookBorrowing, BookBorrowingBookStatus
from domain.user.entities.user_entity import User
from errors.business_error import BusinessError

module_path = RemoveBookFineUseCase.__module__


class TestRemoveBookFineUseCase(TestCase):

    def test_remove_fine_should_succeed(self):
        book = Book(
            user=User(id='5f263d7f1362bc7a1fa2548b')
        )

        flask_request = MagicMock(
            logged_user=MagicMock(user_id=ObjectId('5f263d7f1362bc7a1fa2548b'))
        )

        book_borrowing = BookBorrowing()

        with patch.object(Book, 'first', return_value=book), \
                patch(f'{module_path}.request', flask_request), \
                patch.object(BookBorrowing, 'first', return_value=book_borrowing), \
                patch.object(Book, 'save', spec=True) as save_book, \
                patch.object(BookBorrowing, 'save', spec=True) as save_book_borrowing:
            RemoveBookFineUseCase(
                book_id='5f260ab7cbd8d651ca92dd80',
                user_id='5f25f5963d9eb32fd95f149e'
            ).exec()

            self.assertEqual(BookStatus.AVAILABLE.value, book.status)
            save_book.assert_called_once()
    
            self.assertEqual(BookBorrowingBookStatus.CLOSED.value, book_borrowing.status)
            save_book_borrowing.assert_called_once()

    def test_remove_fine_given_non_existent_book_should_raise_error(self):
        with patch.object(Book, 'first', return_value=None):
            try:
                RemoveBookFineUseCase(
                    book_id='5f260ab7cbd8d651ca92dd80',
                    user_id='5f25f5963d9eb32fd95f149e'
                ).exec()

                self.fail()
            except BusinessError as e:
                self.assertEqual(BusinessError.BOOK_NOT_FOUND, e.code)

    def test_remove_fine_with_book_that_doesnt_belong_to_you_should_raise_error(self):
        book = Book(
            user=User(id='5f263d7f1362bc7a1fa2548b')
        )

        flask_request = MagicMock(
            logged_user=MagicMock(user_id='5f263d7d1362bc7a1fa2548a')
        )

        with patch.object(Book, 'first', return_value=book), \
                patch(f'{module_path}.request', flask_request):
            try:
                RemoveBookFineUseCase(
                    book_id='5f260ab7cbd8d651ca92dd80',
                    user_id='5f25f5963d9eb32fd95f149e'
                ).exec()

                self.fail()
            except BusinessError as e:
                self.assertEqual(BusinessError.BOOK_DOESNT_BELONG_TO_USER, e.code)

    def test_remove_fine_that_doesnt_exist_should_raise_error(self):
        book = Book(
            user=User(id='5f263d7f1362bc7a1fa2548b')
        )

        flask_request = MagicMock(
            logged_user=MagicMock(user_id=ObjectId('5f263d7f1362bc7a1fa2548b'))
        )

        with patch.object(Book, 'first', return_value=book), \
                patch(f'{module_path}.request', flask_request), \
                patch.object(BookBorrowing, 'first', return_value=None):
            try:
                RemoveBookFineUseCase(
                    book_id='5f260ab7cbd8d651ca92dd80',
                    user_id='5f25f5963d9eb32fd95f149e'
                ).exec()

                self.fail()
            except BusinessError as e:
                self.assertEqual(BusinessError.BOOK_BORROWING_NOT_FOUND, e.code)
