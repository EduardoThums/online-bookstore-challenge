from mongoengine import ReferenceField

from domain.base.entities.base_entity import BaseEntity
from domain.book.entities.book_entity import Book
from domain.user.entities.user_entity import User


class BookBorrowing(BaseEntity):

    meta = {
        'collection': 'book_borrowing'
    }

    book = ReferenceField(Book, required=True)

    user = ReferenceField(User, required=True)
