from typing import Optional

from jwt import encode, decode

from helpers import ConfigHelper


class JwtHelper:

    @staticmethod
    def encode_token(user_id: str, user_email: str, user_name: str) -> str:
        payload = {
            'user_id': user_id,
            'user_email': user_email,
            'user_name': user_name
        }

        token = encode(
            algorithm='HS256',
            key=ConfigHelper.SECRET_KEY,
            payload=payload
        )

        return token.decode('utf-8')

    @staticmethod
    def decode_token(token: str) -> Optional[dict]:
        try:
            token = decode(
                algorithms=['HS256'],
                key=ConfigHelper.SECRET_KEY,
                jwt=token
            )

            return token

        except Exception:
            return None
