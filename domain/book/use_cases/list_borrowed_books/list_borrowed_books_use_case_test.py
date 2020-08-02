from unittest import TestCase
from unittest.mock import patch, MagicMock

from bson import ObjectId

from domain.book.entities.book_entity import Book
from domain.book.use_cases.list_borrowed_books.list_borrowed_books_use_case import ListBorrowedBooksUseCase
from domain.book_borrowing.entities.book_borrowing_entity import BookBorrowing
from domain.user.entities.user_entity import User

module_path = ListBorrowedBooksUseCase.__module__


class TestListBorrowedBooksUseCase(TestCase):

    def test_list_borrowed_books_should_succeed(self):
        flask_request = MagicMock(
            logged_user=MagicMock(user_id='5f260aadcbd8d651ca92dd7f')
        )

        books = [Book()]

        book_borrowing = BookBorrowing(
            user=User(id='5f260ab7cbd8d651ca92dd80')
        )

        estimate_borrowing_fine = MagicMock(
            total_fine=10
        )

        with patch(f'{module_path}.request', flask_request), \
                patch.object(Book, 'objects', return_value=books), \
                patch.object(BookBorrowing, 'first', return_value=book_borrowing), \
                patch(f'{module_path}.EstimateBorrowingFineUseCase', return_value=estimate_borrowing_fine):
            use_case = ListBorrowedBooksUseCase()
            use_case.exec()

            borrowed_book = use_case.borrowed_books[0]

            self.assertEqual(books[0], borrowed_book.book)
            self.assertEqual(10, borrowed_book.total_fine)
            self.assertEqual(ObjectId('5f260ab7cbd8d651ca92dd80'), borrowed_book.borrowed_to_user)
