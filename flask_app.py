from flask import Flask

from helpers.database.database_helper import DatabaseHelper
from routes import auth_middleware, book_middleware, user_middleware

app = Flask(__name__)

app.register_blueprint(book_middleware)
app.register_blueprint(user_middleware)
app.register_blueprint(auth_middleware)


@app.before_first_request
def connect_to_database():
    DatabaseHelper.connect()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
