from jwt import encode, decode

_SECRET_KEY = '3ptKHs8qdsrPkih2i0aQZelY06rIKe3swDgXIFz2EGIXCnusSceiVB9pcVSARQ2lHCMkksVkF8faa7MQWnmqhcpd56NxVDxQhgVGdTGP8ZpDAYnFY1ANkTJqqvqsHs'


class JwtHelper:

    @staticmethod
    def encode_token(user_email: str, user_name: str) -> str:
        payload = {
            'user_email': user_email,
            user_name: user_name
        }

        token = encode(
            algorithm='HS256',
            key=_SECRET_KEY,
            payload=payload
        )

        return token.decode('utf-8')

    @staticmethod
    def decode_token(token: str) -> dict:
        token = decode(
            algorithms=['HS256'],
            key=_SECRET_KEY,
            jwt=token
        )

        return token
