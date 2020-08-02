from bson import ObjectId
from mongoengine import connect

from helpers import ConfigHelper


class DatabaseHelper:

    @staticmethod
    def connect():
        connect('online-bookstore',  host=ConfigHelper.MONGODB_HOST)

    @staticmethod
    def convert_to_object_id(string_id) -> ObjectId:
        is_valid = ObjectId.is_valid(string_id)

        if is_valid:
            return ObjectId(string_id)

        else:
            raise Exception("Given id its not in object ID format")
