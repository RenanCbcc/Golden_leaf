import unittest
from persistence.usersDAO import ClientDAO, ClerkDAO
from persistence.connection import Connection
from transference.users import Client, Clerk


class TestCaseIncludeUser(unittest.TestCase):

    def test_save_client(self):
        clientDAO = ClientDAO(Connection())
        cl = Client("Dorothy", "King", "72259372007")
        cl = clientDAO.save(cl)
        same = clientDAO.search(cl.id)
        print(same.identification)
        self.assertEqual(cl, same)

    def test_save_another_client(self):
        clientDAO = ClientDAO(Connection())
        cl = Client("Caelan","Corrigan","63755750449")
        cl = clientDAO.save(cl)
        same = clientDAO.search(cl.id)
        print(same.identification)
        self.assertEqual(cl, same)

    def test_save_clerk(self):
        clerkDAO = ClerkDAO(Connection())
        cl = Clerk("Nonato", "nonato@vendinha.com", "passwd789", "31710548410")
        cl = clerkDAO.save(cl)
        same = clerkDAO.search(cl.id)
        self.assertEqual(cl, same)
