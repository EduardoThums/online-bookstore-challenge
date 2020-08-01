from flask import Blueprint, jsonify

from domain.book.entities.book_entity import Book
from helpers.serializer.serializer_helper import SerializerHelper
from routes.middlewares.required_logged_user.required_logged_user_middleware import require_logged_user

book_middleware = Blueprint('book_middleware', __name__)


@book_middleware.route('/books', methods=['GET'])
@require_logged_user
def list_all_books():
    books = SerializerHelper.serialize(Book.objects)

    return jsonify({'books': books}), 200
