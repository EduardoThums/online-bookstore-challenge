from typing import List

from mongoengine import Document, DateTimeField

from helpers.database.database_helper import DatabaseHelper
from helpers.date.date_helper import DateHelper
from helpers.serializer.serializer_helper import Serializable


class BaseEntity(Document, Serializable):

    meta = {
        'abstract': True
    }

    created_at = DateTimeField(required=True, default=DateHelper.now())

    last_updated_at = DateTimeField(required=True, default=DateHelper.now())

    def __serialize__(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'last_updated_at': self.last_updated_at
        }

    @classmethod
    def first(cls, **filters):
        if 'id' in filters:
            filters['id'] = DatabaseHelper.convert_to_object_id(filters['id'])

        try:
            first_document = cls.objects.get(**filters)

            return first_document

        except Exception:
            return None

    @classmethod
    def first_aggregation(cls, pipeline: List[dict]):
        try:
            aggregation_result = cls.objects.aggregate(pipeline)

            return next(aggregation_result)

        except Exception:
            return None
