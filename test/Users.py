import unittest
from persistence.usersDAO import ClientDAO
from persistence.connection import Connection
from transference.users import Client,Clerk

class MyTestCase(unittest.TestCase):

    def test_save_client(self):
        userDAO = ClientDAO(Connection())
        cl = Client("Cristiane","Isis Drumond","63554421464",True)
        cl = userDAO.save(cl)
        self.assertEqual(cl.id, userDAO.search(cl.id))


"""
if __name__ == '__main__':
    unittest.main()
"""