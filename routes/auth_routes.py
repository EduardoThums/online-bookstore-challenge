from flask import Blueprint, jsonify, request

from domain.user.use_cases.login.login_use_case import LoginUseCase

auth_middleware = Blueprint('auth_middleware', __name__)


@auth_middleware.route('/login', methods=['POST'])
def login():
    request_json = request.get_json()

    email = request_json['email']
    password = request_json['password']

    use_case = LoginUseCase(
        email=email,
        password=password
    )
    use_case.exec()

    return jsonify({'access_token': use_case.access_token}), 201
