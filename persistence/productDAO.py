from transference.products import Product

SAVE_PRODUCT = 'INSERT INTO Product (title, name, price, code) VALUES (%s, %s, %i, %s)'
DELETE_PRODUCT = 'DELETE FROM Product WHERE id = %d'
ALTER_PRODUCT = 'UPDATE Product SET title = %s name = %s, price = %s, code = %s WHERE id = %i'
SEARCH_PRODUCT = 'SELECT * FROM Product WHERE id = %d'
SEARCH_CODE = 'SELECT * FROM Product WHERE code = %s'
LISTING_PRODUCTS='SELECT * FROM Product'

SAVE_ITEM = 'INSERT INTO Product (id_demand,id_product,quantity) VALUES (%i, %i, %f)'

class ProductDAO(object):

    def __init__(self, connection):
        self.__connection = connection

    def save(self, product):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(SAVE_PRODUCT, (product.title, product.name, product.price, product.code))
        self.____connection.confirm_transaction()
        return product

    def delete(self, id):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(DELETE_PRODUCT, (id))
        self.__connection.confirm_transaction()

    def alter(self, product):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(ALTER_PRODUCT, (product.title, product.name, product.price, product.code))
        self.__connection.confirm_transaction()
        return product

    def search(self, id):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(SEARCH_PRODUCT, (id))
        tuple = cursor.fetchone()
        return Product(tuple[1], tuple[2], tuple[3], tuple[4], id=tuple[0])

    def search_code(self, code):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(SEARCH_CODE, (code))
        tuple = cursor.fetchone()
        return Product(tuple[1], tuple[2], tuple[3], tuple[4], id=tuple[0])


    def show_all(self):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(LISTING_PRODUCTS)
        products = self.__tuple_to_addesses(cursor.fetchall())
        return products

    def __tuple_to_products(self, tuples):
        def __map_tuple_to_object(tuple):
            return Product(tuple[1], tuple[2], tuple[3],tuple[4], id=tuple[0])

        return list(map(__map_tuple_to_object,tuples))





