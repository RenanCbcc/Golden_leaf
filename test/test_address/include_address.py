import unittest

from persistence.addressDAO import AddressDAO
from persistence.connection import Connection
from transference.address import Address


class TestCaseIncludeAddresses(unittest.TestCase):

    @unittest.skip
    def test_include_address(self):
        daoAddress = AddressDAO(Connection())
        ad = Address("1", "Passagem Gama Malcher", "482", "66085390")
        daoAddress.save(ad)
        same = daoAddress.search(ad.id_client)
        self.assertEqual(ad.place, same.place)

    @unittest.skip
    def test_include_another_address(self):
        daoAddress = AddressDAO(Connection())
        ad = Address("3", "Vila Carlos", "562", "66645565")
        daoAddress.save(ad)
        same = daoAddress.search(ad.id_client)
        self.assertEqual(ad, same)

    @unittest.skip
    def test_alter_address(self):
        daoAddress = AddressDAO(Connection())
        ad = Address("1", "Passagem Maria da Glória", "650", "66840230")
        daoAddress.alter(ad)
        same = daoAddress.search(ad.id_client)
        self.assertEqual(ad, same)

    @unittest.skip
    def test_deleteaddress(self):
        daoAddress = AddressDAO(Connection())
        daoAddress.delete('1')
        ad = daoAddress.search(1)
        self.assertIsNone(ad)
