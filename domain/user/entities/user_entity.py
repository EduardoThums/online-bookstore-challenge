from mongoengine import StringField

from domain.base.entities.base_entity import BaseEntity


class User(BaseEntity):

    meta = {
        'collection': 'users'
    }

    email = StringField(required=True, unique=True)

    name = StringField(required=True, min_length=2, max_length=100)

    password = StringField(required=True)

    def __serialize__(self):
        return {
            **super(User, self).__serialize__(),
            'email': self.email,
            'name': self.name,
            'password': self.password
        }
