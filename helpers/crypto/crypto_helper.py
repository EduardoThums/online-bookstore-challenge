from bcrypt import hashpw, gensalt, checkpw


class CryptoHelper:

    @staticmethod
    def hash_password(password: str) -> str:
        encoded_password = password.encode('utf-8')

        hashed_password = hashpw(encoded_password, gensalt())

        return hashed_password

    @staticmethod
    def check_password(password: str, hashed_password: str) -> bool:
        return checkpw(password, hashed_password)
