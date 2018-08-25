import unittest
import datetime
from persistence.connection import Connection
from persistence.demandDAO import DemandDAO
from transference.demands import Demand, Item


class TestCaseOrder(unittest.TestCase):

    def test_include_Order(self):
        dao = DemandDAO(Connection())
        items = [Item(1, 2), Item(2, 1), Item(3, 0.5)]
        order = Demand(datetime.date.today(),
                       datetime.datetime.now().strftime("%H:%M:%S")
                       , 1, 9, items)
        same = dao.save(order)

        self.assertEqual(same, order)
