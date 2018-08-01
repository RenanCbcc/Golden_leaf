from transference.products import Product

SAVE_PRODUCT = 'INSERT INTO Product (title, name, price, code) values (%s, %s, %d, %s)'
DELETE_PRODUCT = 'DELETE FROM Product WHERE id = %d'
ALTER_PRODUCT = 'UPDATE Product SET name = %s, SET price = %s, SET code = %s WHERE id = %d'
SEARCH_PRODUCT = 'SELECT * FROM Product WHERE id = ?'


class ProductDAO(object):

    def __init__(self, connection):
        self.__connection = connection

    def save(self, product):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(SAVE_PRODUCT, (product.id_user, product.place, product.number, product.zip_code))
        self.____connection.confirm_transaction()
        return product

    def delete(self, id_user):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(DELETE_PRODUCT, (id_user))
        self.__connection.confirm_transaction()

    def alter(self, product):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(ALTER_PRODUCT, (product.place, product.number, product.zip_code))
        self.__connection.confirm_transaction()
        return product

    def search(self, id_user):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(SEARCH_PRODUCT, (id_user))
        tuple = cursor.fetchone()
        return Product(tuple[1], tuple[2], tuple[3], id=tuple[0])
