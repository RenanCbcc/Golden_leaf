from transference.demands import Demand,Item

SAVE_DEMAND = 'INSERT INTO Demand (date, time, id_client, id_clerk) VALUES (%s, %s, %d, %d)'
DELETE_DEMAND = 'DELETE FROM Demand WHERE id = %d'
SEARCH_DEMAND = 'SELECT * FROM Product WHERE id_client = %d'
SEARCH_DEMAND = 'SELECT * FROM Product WHERE code = %s'
LISTING_DEMAND='SELECT d.id,d.date,d.time,c.name,a.name FROM Demand d ,Client c,Clerk a ' \
               'WHERE d.id_client =c.id_user AND d.id_clerk = a.id_user'

SAVE_ITEM = 'INSERT INTO Item (id_demand,id_product,quantity) VALUES (%d, %d, %f)'
DELETE_ITEM = 'DELETE FROM Item WHERE id_demand = %d AND id_product = %d'
ALTER_ITEM = 'UPDATE Item SET quantity = %f WHERE id_demand = %d'
SEARCH_ITEM = 'SELECT * FROM Item WHERE id = %d'
LISTING_ITEM = 'SELECT * FROM Item'


class DemandDAO(object):

    def __init__(self, connection):
        self.__connection = connection

    def save(self, demand):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(SAVE_DEMAND, (demand.date, demand.time, demand.id_client, demand.id_clerk))
        itemdao = ItemDAO(self.__connection)
        for item in demand.items:
            itemdao.save(item)
        del(itemdao)
        self.____connection.confirm_transaction()
        return demand

    def delete(self, id):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(DELETE_DEMAND, (id))
        self.__connection.confirm_transaction()

    def search(self, id):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(SEARCH_DEMAND, (id))
        tuple = cursor.fetchone()
        return Demand(tuple[1], tuple[2], tuple[3], tuple[4], id=tuple[0])


    def show_all(self):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(LISTING_DEMAND)
        products = self.__tuple_to_addesses(cursor.fetchall())
        return products

    def __tuple_to_products(self, tuples):
        def __map_tuple_to_object(tuple):
            return Demand(tuple[1], tuple[2], tuple[3], tuple[4], id=tuple[0])

        return list(map(__map_tuple_to_object, tuples))


class ItemDAO(object):

    def __init__(self, connection):
        self.__connection = connection

    def save(self, item):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(SAVE_ITEM, (item.id_demand, item.id_product, item.quantity))


    def delete(self, id):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(DELETE_ITEM, (id))


    def alter(self, product):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(ALTER_ITEM, (product.title, product.name, product.price, product.code))
        self.__connection.confirm_transaction()
        return product

    def search(self, id):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(SEARCH_ITEM, (id))
        tuple = cursor.fetchone()
        return Item(tuple[1], tuple[2], tuple[3])

    def show_all(self):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(LISTING_ITEM)
        products = self.__tuple_to_addesses(cursor.fetchall())
        return products

    def __tuple_to_products(self, tuples):
        def __map_tuple_to_object(tuple):
            return Item(tuple[1], tuple[2], tuple[3])

        return list(map(__map_tuple_to_object, tuples))

