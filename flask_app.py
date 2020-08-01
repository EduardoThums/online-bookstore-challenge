from flask import Flask, jsonify

from erros.authentication_error import AuthenticationError
from erros.business_error import BusinessError
from helpers.database.database_helper import DatabaseHelper
from helpers.serializer.serializer_helper import SerializerHelper
from routes import auth_middleware, book_middleware, user_middleware

app = Flask(__name__)

app.register_blueprint(book_middleware)
app.register_blueprint(user_middleware)
app.register_blueprint(auth_middleware)


@app.before_first_request
def connect_to_database():
    DatabaseHelper.connect()


def handle_base_error(e, http_code: int):
    response = SerializerHelper.serialize(e)

    return jsonify(response), http_code


@app.errorhandler(BusinessError)
def handle_business_error(e):
    return handle_base_error(e, 422)


@app.errorhandler(AuthenticationError)
def handle_authentication_error(e):
    return handle_base_error(e, 403)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
