from enum import Enum

from mongoengine import LazyReferenceField, StringField

from domain.base.entities.base_entity import BaseEntity
from domain.book.entities.book_entity import Book
from domain.user.entities.user_entity import User


class BookBorrowingBookStatus(Enum):
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'


class BookBorrowing(BaseEntity):

    meta = {
        'collection': 'book_borrowing'
    }

    book = LazyReferenceField(Book, required=True)

    user = LazyReferenceField(User, required=True)

    status = StringField(required=True, default=BookBorrowingBookStatus.OPEN.value)
