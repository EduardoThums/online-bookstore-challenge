from enum import Enum

from mongoengine import StringField, IntField, ReferenceField

from domain.base.entities.base_entity import BaseEntity
from domain.user.entities.user_entity import User


class BookStatus(Enum):
    AVAILABLE = 'AVAILABLE'
    BORROWED = 'BORROWED'


class Book(BaseEntity):

    meta = {
        'collection': 'books'
    }

    title = StringField(required=True, min_length=2, max_length=100, unique=True)

    description = StringField(min_length=2, max_length=500)

    author = StringField(min_length=2, max_length=50)

    cost = IntField(required=True)

    user = ReferenceField(User, required=False)

    status = StringField(required=True, default=BookStatus.AVAILABLE.value)

    def __serialize__(self):
        return {
            **super(Book, self).__serialize__(),
            'title': self.title,
            'description': self.description,
            'author': self.author,
            'cost': self.cost,
            'user': self.user,
            'status': self.status
        }
