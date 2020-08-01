from flask import request

from domain.base.use_cases.base_use_case import BaseUseCase
from domain.book.entities.book_entity import Book, BookStatus
from domain.book_borrowing.entities.book_borrowing_entity import BookBorrowing
from domain.book_borrowing.entities.book_borrowing_entity import BookBorrowingBookStatus
from domain.book_borrowing.use_cases.estimate_borrowing_fine.estimate_borrowing_fine_use_case import \
    EstimateBorrowingFineUseCase
from erros.business_error import BusinessError
from helpers.database.database_helper import DatabaseHelper


class ReturnBookUseCase(BaseUseCase):

    def __init__(self, book_id: str):
        self.book_id = DatabaseHelper.convert_to_object_id(book_id)

    def exec(self):
        book = Book.first(id=self.book_id)

        if book is None:
            raise BusinessError(code=BusinessError.BOOK_NOT_FOUND)

        logged_user = request.logged_user

        book_borrowing = BookBorrowing.first(
            book=self.book_id,
            user=logged_user.user_id,
            status=BookBorrowingBookStatus.OPEN.value
        )

        if book_borrowing is None:
            raise BusinessError(code=BusinessError.BOOK_BORROWING_NOT_FOUND)

        use_case = EstimateBorrowingFineUseCase(
            borrow_date=book_borrowing.created_at,
            book_cost=book.cost
        )
        use_case.exec()

        if use_case.total_fine > 0:
            raise BusinessError(code=BusinessError.NOT_ALLOWED_TO_RETURN_BOOK_WITH_OPEN_FINE)

        book_borrowing.status = BookBorrowingBookStatus.CLOSED.value
        book_borrowing.save()

        book.status = BookStatus.AVAILABLE.value
        book.save()
