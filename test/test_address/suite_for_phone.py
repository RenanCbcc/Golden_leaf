import unittest

from persistence.addressDAO import PhoneDAO
from persistence.connection import Connection
from transference.addresses import Phone


class TestCasePhone(unittest.TestCase):

    @unittest.skip
    def test_include_phone(self):
        daoPhone = PhoneDAO(Connection())
        ad = daoPhone.save(Phone("1", "91984292065", True))
        same = daoPhone.search(ad.id_user)
        self.assertEqual(ad.phone_number, same.phone_number)

    @unittest.skip
    def test_include_another_phone(self):
        daoPhone = PhoneDAO(Connection())
        ad = daoPhone.save(Phone("2", "91984292065", True))
        same = daoPhone.search(ad.id_user)
        self.assertEqual(ad.phone_number, same.phone_number)

    @unittest.skip
    def test_alter_phone_number(self):
        daoPhone = PhoneDAO(Connection())
        ad = daoPhone.alter(Phone("2", "91992099760", True))
        same = daoPhone.search(ad.id_user)
        self.assertEqual(ad.phone_number, same.phone_number)

    @unittest.skip
    def test_show_phone_number(self):
        daoPhone = PhoneDAO(Connection())
        ad = daoPhone.alter(Phone("2", "91992099760", True))
        same = daoPhone.search(ad.id_user)
        self.assertEqual(ad.phone_number, same.phone_number)
