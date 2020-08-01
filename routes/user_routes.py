from flask import Blueprint, jsonify, request

from domain.user.use_cases.register_user.register_user_use_case import RegisterUserUseCase

user_middleware = Blueprint('user_middleware', __name__)


@user_middleware.route('/users', methods=['POST'])
def register_user():
    request_json = request.get_json()

    email = request_json['email']
    password = request_json['password']
    name = request_json['name']

    RegisterUserUseCase(
        email=email,
        password=password,
        name=name
    ).exec()

    return jsonify(), 201
