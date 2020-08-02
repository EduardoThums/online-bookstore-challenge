from unittest import TestCase
from unittest.mock import patch

from domain.book.entities.book_entity import Book
from domain.book.use_cases.list_all_books.list_all_books_use_case import ListAllBooksUseCase
from domain.user.entities.user_entity import User


class TestListAllBooksUseCase(TestCase):

    def test_list_all_books_should_succeed(self):
        books = [
            Book(
                title='title',
                description='description',
                author='author',
                user=User()
            ),
            Book(
                title='title',
                description='description',
                author='author',
                user=User()
            )
        ]

        with patch.object(Book, 'objects', books):
            use_case = ListAllBooksUseCase()
            use_case.exec()

            self.assertEqual(2, len(use_case.books))
