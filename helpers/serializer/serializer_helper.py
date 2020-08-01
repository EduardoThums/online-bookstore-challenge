from datetime import datetime
from enum import Enum

from bson import ObjectId
from mongoengine import QuerySet

from helpers.date.date_helper import DateHelper


class Serializable:
    def __serialize__(self):
        raise NotImplementedError()

    @classmethod
    def deserialize(cls, data):
        return data


class SerializerHelper:
    @staticmethod
    def serialize_dict_key(value):
        return SerializerHelper.serialize(value)

    @staticmethod
    def serialize_dict(data: dict):
        result = {}

        for key, value in data.items():
            result[key] = SerializerHelper.serialize_dict_key(value)

        return result

    @staticmethod
    def serialize_list(data: list):
        result = []

        for item in data:
            result.append(SerializerHelper.serialize(item))

        return result

    @staticmethod
    def serialize_datetime(data: datetime):
        return DateHelper.serialize(data)

    @staticmethod
    def serialize_object_id(data: ObjectId):
        return str(data)

    @staticmethod
    def serialize_enum(data: Enum):
        return data.value

    @staticmethod
    def serialize_serializable(data: Serializable):
        return SerializerHelper.serialize(
            data.__serialize__()
        )

    @staticmethod
    def serialize(data, ignore_serializable=False):
        if not ignore_serializable and isinstance(data, Serializable):
            return SerializerHelper.serialize_serializable(data)

        if isinstance(data, dict):
            return SerializerHelper.serialize_dict(data)

        if isinstance(data, list):
            return SerializerHelper.serialize_list(data)

        if isinstance(data, datetime):
            return SerializerHelper.serialize_datetime(data)

        if isinstance(data, ObjectId):
            return SerializerHelper.serialize_object_id(data)

        if isinstance(data, Enum):
            return SerializerHelper.serialize_enum(data)

        if isinstance(data, QuerySet):
            return SerializerHelper.serialize_list(list(data))

        return data
