import unittest

from persistence.connection import Connection
from persistence.productDAO import ProductDAO
from transference.products import Product


class TestCaseIncludeProduct(unittest.TestCase):

    @unittest.skip
    def test_include_product(self):
        productDao = ProductDAO(Connection())
        pd = Product("Arroz","Fazanda",3.50,'001')
        pd.id=1
        productDao.save(pd)
        same = productDao.search(pd.id)
        self.assertEqual(pd, same)

    @unittest.skip
    def test_include_another_product(self):
        productDao = ProductDAO(Connection())
        pd = Product("Feijão carioca","Tio pedro",5.50,'003')
        pd.id=2
        productDao.save(pd)
        same = productDao.search(pd.id)
        self.assertEqual(pd, same)


    def test_list_products(self):
        productDao = ProductDAO(Connection())
        pd = productDao.show_all()
        for p in pd:
            print(p)
        self.assertIsNotNone(pd,"Cadê osprodutos?")






