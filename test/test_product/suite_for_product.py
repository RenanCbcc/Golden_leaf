import unittest
from app.models.tables import Product, db


class TestCaseIncludeProduct(unittest.TestCase):

    @unittest.skip
    def test_include_product(self):
        pd = Product("Arroz", "Fazanda", 3.50, '001')
        db.session.add(pd)
        db.session.commit()
        db.session.refresh(pd)
        same = Product.query.filter_by(id=pd.id).one()
        self.assertEqual(pd, same)

    @unittest.skip
    def test_include_another_product(self):
        pd = Product("Feijão carioca", "Tio pedro", 5.50, '003')
        db.session.add(pd)
        db.session.commit()
        db.session.refresh(pd)
        same = Product.query.filter_by(id=pd.id).one()
        self.assertEqual(pd, same)
