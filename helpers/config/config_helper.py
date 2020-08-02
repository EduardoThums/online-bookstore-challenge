import os


class ConfigHelper:

    MONGODB_HOST = None
    SECRET_KEY = None

    @classmethod
    def load_environment_variables(cls):
        cls.MONGODB_HOST = cls._get_environment_variable('MONGODB_HOST')
        cls.SECRET_KEY = cls._get_environment_variable('SECRET_KEY')

    @staticmethod
    def _get_environment_variable(name: str):
        return os.environ.get(name, None)
