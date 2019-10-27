import unittest
from app.models import Address, db


class TestCaseIncludeAddresses(unittest.TestCase):

    @unittest.skip
    def test_include_address(self):
        ad = Address("1", "Passagem Gama Malcher", "482", "66085390")
        db.session.add(ad)
        db.session.commit()
        db.session.refresh(ad)
        same = Address.query.filter_by(id=ad.id).one()
        self.assertEqual(ad, same)

    @unittest.skip
    def test_include_another_address(self):
        ad = Address("3", "Vila Carlos", "562", "66645565")
        db.session.add(ad)
        db.session.commit()
        db.session.refresh(ad)
        same = Address.query.filter_by(id=ad.id).one()
        self.assertEqual(ad, same)

    @unittest.skip
    def test_alter_address(self):
        pass

    @unittest.skip
    def test_deleteaddress(self):
        pass
