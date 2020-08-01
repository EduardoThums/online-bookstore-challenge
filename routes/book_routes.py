from flask import Blueprint, jsonify

from domain.book.entities.book_entity import Book
from helpers.serializer.serializer_helper import SerializerHelper

book_middleware = Blueprint('book_routes', __name__)


@book_middleware.route('/books', methods=['GET'])
def list_all_books():
    book = Book(
        title='asdasdasd',
        cost=100
    )
    book.save()

    return jsonify(SerializerHelper.serialize(Book.objects)), 200
