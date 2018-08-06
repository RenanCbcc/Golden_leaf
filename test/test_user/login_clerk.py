import unittest

from persistence.connection import Connection
from persistence.usersDAO import ClerkDAO


class MyTestCase(unittest.TestCase):
    def test_something(self):
        clerkDAO = ClerkDAO(Connection())
        same = clerkDAO.login("renan@vendinha.com")
        self.assertIsNotNone(same)
        self.assertEqual("renan@vendinha.com", same.email)
        self.assertEqual("passwd123",same.password)

