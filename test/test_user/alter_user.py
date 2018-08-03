import unittest
from persistence.usersDAO import ClientDAO, ClerkDAO
from persistence.connection import Connection


class TestCaseAlterUser(unittest.TestCase):


    def test_alter_client(self):
        clientDAO = ClientDAO(Connection())
        cl = clientDAO.search(3)
        cl.name = "Jane"
        cl.surname = "East"
        cl.status = False
        clientDAO.alter(cl)
        same = clientDAO.search(cl.id)
        self.assertEqual(cl,same)
        self.assertEqual(cl.name,same.name)


    def test_alter_clerk(self):
        clerkDAO = ClerkDAO(Connection())
        cl = clerkDAO.search(2)
        cl.name= 'Ruan'
        cl.email = "ruan@vendinha.com"
        cl.password = "passwd456"
        print(cl)
        clerkDAO.alter(cl)
        same = clerkDAO.search(cl.id)
        print(same)
        self.assertEqual(cl, same)
        self.assertEqual(cl.name, same.name)


