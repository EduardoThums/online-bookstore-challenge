from flask import request

from domain.base.use_cases.base_use_case import BaseUseCase
from domain.book.entities.book_entity import Book, BookStatus
from domain.book_borrowing.entities.book_borrowing_entity import BookBorrowing, BookBorrowingBookStatus
from errors.business_error import BusinessError
from helpers.database.database_helper import DatabaseHelper


class RemoveBookFineUseCase(BaseUseCase):

    def __init__(self, book_id: str, user_id: str):
        self.book_id = DatabaseHelper.convert_to_object_id(book_id)
        self.user_id = DatabaseHelper.convert_to_object_id(user_id)

    def exec(self):
        book = Book.first(
            id=self.book_id
        )

        if book is None:
            raise BusinessError(code=BusinessError.BOOK_NOT_FOUND)

        if book.user.id != request.logged_user.user_id:
            raise BusinessError(code=BusinessError.BOOK_DOESNT_BELONG_TO_USER)

        book_borrowing = BookBorrowing.first(
            book=self.book_id,
            user=self.user_id,
            status=BookBorrowingBookStatus.OPEN.value
        )

        if book_borrowing is None:
            raise BusinessError(code=BusinessError.BOOK_BORROWING_NOT_FOUND)

        book.status = BookStatus.AVAILABLE.value
        book.save()

        book_borrowing.status = BookBorrowingBookStatus.CLOSED.value
        book_borrowing.save()
