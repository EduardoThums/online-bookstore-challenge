from flask import Blueprint, jsonify, request

from domain.book.entities.book_entity import Book
from domain.book.use_cases.borrow_book.borrow_book_use_case import BorrowBookUseCase
from domain.book.use_cases.register_book.register_book_use_case import RegisterBookUseCase
from helpers.serializer.serializer_helper import SerializerHelper
from routes.middlewares.required_logged_user.required_logged_user_middleware import require_logged_user

book_middleware = Blueprint('book_middleware', __name__)


@book_middleware.route('/books', methods=['GET'])
@require_logged_user
def list_all_books():
    books = SerializerHelper.serialize(Book.objects)

    return jsonify({'books': books}), 200


@book_middleware.route('/books', methods=['POST'])
@require_logged_user
def register_book():
    request_json = request.get_json()

    title = request_json['title']
    description = request_json.get('description')
    author = request_json.get('author')
    cost = request_json['cost']

    use_case = RegisterBookUseCase(
        title=title,
        description=description,
        author=author,
        cost=cost
    )
    use_case.exec()

    return jsonify(SerializerHelper.serialize(use_case.registered_book)), 201


@book_middleware.route('/books/<book_id>', methods=['POST'])
@require_logged_user
def borrow_book(book_id: str):
    BorrowBookUseCase(
        book_id=book_id
    ).exec()

    return jsonify(), 201
