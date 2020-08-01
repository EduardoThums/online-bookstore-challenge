from unittest import TestCase
from unittest.mock import patch, MagicMock

from domain.book.entities.book_entity import Book, BookStatus
from domain.book_borrowing.entities.book_borrowing_entity import BookBorrowing, BookBorrowingBookStatus
from domain.book_borrowing.use_cases.return_book.return_book_use_case import ReturnBookUseCase
from errors.business_error import BusinessError
from helpers.date.date_helper import DateHelper

module_path = ReturnBookUseCase.__module__


class TestReturnBookUseCase(TestCase):

    def test_return_book_in_the_deadline_should_not_charge_fine(self):
        book = Book()

        book_borrowing = BookBorrowing(
            created_at=DateHelper.now()
        )

        estimate_borrowing_fine = MagicMock(
            total_fine=0
        )

        with patch.object(Book, 'first', return_value=book), \
                patch(f'{module_path}.request'), \
                patch.object(BookBorrowing, 'first', return_value=book_borrowing), \
                patch(f'{module_path}.EstimateBorrowingFineUseCase', return_value=estimate_borrowing_fine), \
                patch.object(BookBorrowing, 'save', spec=True) as save_book_borrowing, \
                patch.object(Book, 'save', spec=True) as save_book:
            ReturnBookUseCase(
                book_id='5f25eac0159cb9dfa8a2e8d2'
            ).exec()

            self.assertEqual(BookBorrowingBookStatus.CLOSED.value, book_borrowing.status)
            save_book_borrowing.assert_called_once()

            self.assertEqual(BookStatus.AVAILABLE.value, book.status)
            save_book.assert_called_once()

    def test_return_book_with_fine_due_delay_should_raise_error(self):
        book = Book()

        book_borrowing = BookBorrowing(
            created_at=DateHelper.now()
        )

        estimate_borrowing_fine = MagicMock(
            total_fine=10
        )

        with patch.object(Book, 'first', return_value=book), \
                patch(f'{module_path}.request'), \
                patch.object(BookBorrowing, 'first', return_value=book_borrowing), \
                patch(f'{module_path}.EstimateBorrowingFineUseCase', return_value=estimate_borrowing_fine):
            try:
                ReturnBookUseCase(
                    book_id='5f25eac0159cb9dfa8a2e8d2'
                ).exec()

                self.fail()
            except BusinessError as e:
                self.assertEqual(BusinessError.NOT_ALLOWED_TO_RETURN_BOOK_WITH_OPEN_FINE, e.code)

    def test_return_book_that_doesnt_exist_should_raise_error(self):
        with patch.object(Book, 'first', return_value=None):
            try:
                ReturnBookUseCase(
                    book_id='5f25eac0159cb9dfa8a2e8d2'
                ).exec()

                self.fail()
            except BusinessError as e:
                self.assertEqual(BusinessError.BOOK_NOT_FOUND, e.code)

    def test_return_book_that_its_not_borrowed_to_you_should_raise_error(self):
        book = Book()

        with patch.object(Book, 'first', return_value=book), \
                patch(f'{module_path}.request'), \
                patch.object(BookBorrowing, 'first_aggregation', return_value=None):
            try:
                ReturnBookUseCase(
                    book_id='5f25eac0159cb9dfa8a2e8d2'
                ).exec()

                self.fail()
            except BusinessError as e:
                self.assertEqual(BusinessError.BOOK_BORROWING_NOT_FOUND, e.code)
