from flask import Flask

from helpers.database.database_helper import DatabaseHelper
from routes.book_routes import book_middleware
from routes.user_routes import user_middleware

app = Flask(__name__)

app.register_blueprint(book_middleware)
app.register_blueprint(user_middleware)


@app.before_first_request
def connect_to_database():
    DatabaseHelper.connect()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
