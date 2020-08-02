from bson import ObjectId
from flask import request

from domain.base.use_cases.base_use_case import BaseUseCase
from domain.book.entities.book_entity import Book, BookStatus
from domain.book_borrowing.entities.book_borrowing_entity import BookBorrowing, BookBorrowingBookStatus
from domain.book_borrowing.use_cases.estimate_borrowing_fine.estimate_borrowing_fine_use_case import \
    EstimateBorrowingFineUseCase
from helpers.serializer.serializer_helper import Serializable


class BorrowedBookDetail(Serializable):

    def __init__(self, book: Book, total_fine: float, borrowed_to_user: ObjectId):
        self.book = book
        self.total_fine = total_fine
        self.borrowed_to_user = borrowed_to_user

    def __serialize__(self):
        return {
            **self.book.__serialize__(),
            'total_fine': self.total_fine,
            'borrowed_to_user': self.borrowed_to_user
        }


class ListBorrowedBooksUseCase(BaseUseCase):

    def __init__(self):
        self.borrowed_books = []

    def exec(self):
        logged_user = request.logged_user

        books = Book.objects(
            status=BookStatus.BORROWED.value,
            user=logged_user.user_id
        )

        borrowed_books = []

        for book in books:
            book_borrowing = BookBorrowing.first(
                book=book.id,
                status=BookBorrowingBookStatus.OPEN.value
            )

            use_case = EstimateBorrowingFineUseCase(
                borrow_date=book_borrowing.created_at
            )
            use_case.exec()

            borrowed_book = BorrowedBookDetail(
                book=book,
                total_fine=use_case.total_fine,
                borrowed_to_user=book_borrowing.user.id
            )

            borrowed_books.append(borrowed_book)

        self.borrowed_books = borrowed_books
