import unittest
from app.models.tables import Client, Clerk, Address, db


class TestCaseIncludeUser(unittest.TestCase):

    def test_save_client(self):
        cl = Client("Dorothy King", "99546-9997", "72259372007")
        db.session.add(cl)
        db.session.commit()
        db.session.refresh(cl)
        same = Client.query.filter_by(id=cl.id).one()
        self.assertEqual(cl, same)

    def test_save_another_client(self):
        cl = Client("Caelan", "Corrigan", "63755750449")
        db.session.add(cl)
        db.session.commit()
        db.session.refresh(cl)
        same = Client.query.filter_by(id=id).one()
        self.assertEqual(cl, same)

    def test_save_clerk(self):
        cl = Clerk("Nonato", "nonato@vendinha.com", "passwd789", "31710548410")
        db.session.add(cl)
        db.session.commit()
        db.session.refresh(cl)
        same = Clerk.query.filter_by(id=id).one()
        self.assertEqual(cl, same)
