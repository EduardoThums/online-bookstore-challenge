from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify

from errors.authentication_error import AuthenticationError
from errors.business_error import BusinessError
from helpers.config.config_helper import ConfigHelper
from helpers.database.database_helper import DatabaseHelper
from helpers.serializer.serializer_helper import SerializerHelper
from routes import auth_middleware, book_middleware, user_middleware

app = Flask(__name__)

app.register_blueprint(book_middleware)
app.register_blueprint(user_middleware)
app.register_blueprint(auth_middleware)


current_directory = Path().absolute()
load_dotenv(f'{current_directory}/.env')

ConfigHelper.load_environment_variables()


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


@app.errorhandler(Exception)
def handle_general_exceptions(e):
    response = {
        'code': 'INTERNAL_SERVER_ERROR',
        'message': 'Something gone wrong internally'
    }

    return jsonify(response), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
