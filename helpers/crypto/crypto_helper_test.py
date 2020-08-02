from unittest import TestCase

from helpers.crypto.crypto_helper import CryptoHelper


class TestCryptoHelper(TestCase):

    def test_hash_password_should_succeed(self):
        password = 'Test123*'

        hashed_password = CryptoHelper.hash_password(password)

        self.assertNotEqual(password, hashed_password)

    def test_check_equals_passwords_should_be_true(self):
        password = 'Test123*'
        hashed_password = CryptoHelper.hash_password(password)

        are_the_passwords_equal = CryptoHelper.check_password(password, hashed_password)

        self.assertTrue(are_the_passwords_equal)

    def test_check_different_passwords_should_be_false(self):
        password = 'Test123*'
        hashed_password = CryptoHelper.hash_password(password)

        another_password = '123'

        are_the_passwords_equal = CryptoHelper.check_password(another_password, hashed_password)

        self.assertFalse(are_the_passwords_equal)
