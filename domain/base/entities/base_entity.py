from mongoengine import Document, DateTimeField

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
