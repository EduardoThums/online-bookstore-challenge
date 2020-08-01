from mongoengine import connect


class DatabaseHelper:

    @staticmethod
    def connect():
        connect('online-bookstore')
