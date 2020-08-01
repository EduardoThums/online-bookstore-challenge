from helpers.serializer.serializer_helper import Serializable


class BaseError(Exception, Serializable):

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message

    def __serialize__(self):
        return {
            'code': self.code,
            'message': self.message
        }
