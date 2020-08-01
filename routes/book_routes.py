from flask import Blueprint, jsonify

from domain.book.entities.book_entity import Book
from helpers.serializer.serializer_helper import SerializerHelper

book_middleware = Blueprint('book_routes', __name__)


@book_middleware.route('/books', methods=['GET'])
def list_all_books():
    books = SerializerHelper.serialize(Book.objects)

    return jsonify({'books': books}), 200
