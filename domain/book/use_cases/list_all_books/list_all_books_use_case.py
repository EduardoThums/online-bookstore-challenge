from domain.base.use_cases.base_use_case import BaseUseCase
from domain.book.entities.book_entity import Book
from helpers.serializer.serializer_helper import SerializerHelper


class ListAllBooksUseCase(BaseUseCase):

    def __init__(self):
        self.books = None

    def exec(self):
        books = SerializerHelper.serialize(Book.objects)

        self.books = books
