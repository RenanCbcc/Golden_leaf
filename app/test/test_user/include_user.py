import unittest
from app.models.tables import Client, Clerk, Address, Product, Order, db


class TestCaseIncludeUser(unittest.TestCase):

    def test_save_client(self):
        cl = Client("Dorothy", "King", "72259372007")
        db.session.add(cl)
        db.session.commit()
        cl = Client.query.filter_by(code=code).first()
        same = clientDAO.search(cl.id)
        self.assertEqual(cl, same)

    def test_save_another_client(self):
        clientDAO = ClientDAO(Connection())
        cl = Client("Caelan", "Corrigan", "63755750449")
        cl = clientDAO.save(cl)
        same = clientDAO.search(cl.id)
        self.assertEqual(cl, same)

    def test_save_clerk(self):
        clerkDAO = ClerkDAO(Connection())
        cl = Clerk("Nonato", "nonato@vendinha.com", "passwd789", "31710548410")
        cl = clerkDAO.save(cl)
        same = clerkDAO.search(cl.id)
        self.assertEqual(cl, same)
