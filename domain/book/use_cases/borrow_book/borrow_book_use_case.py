from flask import request

from domain.base.use_cases.base_use_case import BaseUseCase
from domain.book.entities.book_entity import Book, BookStatus
from domain.book_borrowing.entities.book_borrowing_entity import BookBorrowing
from domain.user.entities.user_entity import User
from erros.business_error import BusinessError
from helpers.database.database_helper import DatabaseHelper


class BorrowBookUseCase(BaseUseCase):

    def __init__(self, book_id):
        self.book_id = DatabaseHelper.convert_to_object_id(book_id)

    def exec(self):
        book_to_be_borrowed = Book.first(id=self.book_id)

        if not book_to_be_borrowed:
            raise BusinessError(code=BusinessError.BOOK_NOT_FOUND)

        if book_to_be_borrowed.user.id == request.logged_user.user_id:
            raise BusinessError(code=BusinessError.NOT_ALLOWED_TO_BORROW_OWN_BOOK)

        if book_to_be_borrowed.status == BookStatus.BORROWED.value:
            raise BusinessError(code=BusinessError.BOOK_CANT_BE_BORROWED)

        user = User.first(id=request.logged_user.user_id)

        book_to_be_borrowed.status = BookStatus.BORROWED.value
        book_to_be_borrowed.save()

        book_borrowing = BookBorrowing(
            book=book_to_be_borrowed,
            user=user
        )

        book_borrowing.save()
