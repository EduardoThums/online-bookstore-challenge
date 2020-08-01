from flask import Blueprint, jsonify, request

from domain.book.use_cases.borrow_book.borrow_book_use_case import BorrowBookUseCase
from domain.book.use_cases.list_all_books.list_all_books_use_case import ListAllBooksUseCase
from domain.book.use_cases.list_borrowed_books.list_borrowed_books_use_case import ListBorrowedBooksUseCase
from domain.book.use_cases.register_book.register_book_use_case import RegisterBookUseCase
from domain.book_borrowing.use_cases.return_book.return_book_use_case import ReturnBookUseCase
from helpers.serializer.serializer_helper import SerializerHelper
from routes.middlewares.required_logged_user.required_logged_user_middleware import require_logged_user

book_middleware = Blueprint('book_middleware', __name__)


@book_middleware.route('/books', methods=['GET'])
@require_logged_user
def list_all_books():
    use_case = ListAllBooksUseCase()
    use_case.exec()

    return jsonify({'books': use_case.books}), 200


@book_middleware.route('/books/borrowed', methods=['GET'])
@require_logged_user
def list_all_borrowed_books():
    use_case = ListBorrowedBooksUseCase()
    use_case.exec()

    return jsonify({'books': SerializerHelper.serialize(use_case.borrowed_books)}), 200


@book_middleware.route('/books', methods=['POST'])
@require_logged_user
def register_book():
    request_json = request.get_json()

    title = request_json['title']
    description = request_json.get('description')
    author = request_json.get('author')

    use_case = RegisterBookUseCase(
        title=title,
        description=description,
        author=author
    )
    use_case.exec()

    return jsonify(SerializerHelper.serialize(use_case.registered_book)), 201


@book_middleware.route('/books/<book_id>/reserve', methods=['POST'])
@require_logged_user
def borrow_book(book_id: str):
    BorrowBookUseCase(
        book_id=book_id
    ).exec()

    return jsonify(), 201


@book_middleware.route('/books/<book_id>/return', methods=['PUT'])
@require_logged_user
def return_book(book_id: str):
    ReturnBookUseCase(
        book_id=book_id
    ).exec()

    return jsonify(), 200

