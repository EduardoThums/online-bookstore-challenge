from flask import request

from domain.base.use_cases.base_use_case import BaseUseCase
from domain.book.entities.book_entity import Book
from errors.business_error import BusinessError


class RegisterBookUseCase(BaseUseCase):

    def __init__(self, title: str, description: str, author: str):
        self.title = title
        self.description = description
        self.author = author

        self.registered_book = None

    def exec(self):
        logged_user = request.logged_user.user_id

        book_with_same_title = Book.first(title=self.title)

        if book_with_same_title is not None:
            raise BusinessError(code=BusinessError.BOOK_ALREADY_REGISTERED)

        new_book = Book(
            title=self.title,
            description=self.description,
            author=self.author,
            user=logged_user
        )
        new_book.save()

        self.registered_book = new_book
