from passlib.handlers.pbkdf2 import pbkdf2_sha256


class CryptoHelper:

    @staticmethod
    def hash_password(password: str) -> str:
        hashed_password = pbkdf2_sha256.hash(password)

        return hashed_password

    @staticmethod
    def check_password(password: str, hashed_password: str) -> bool:
        return pbkdf2_sha256.verify(password, hashed_password)
