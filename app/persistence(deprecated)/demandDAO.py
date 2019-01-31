from data.demands import Demand, Item

SAVE_DEMAND = 'INSERT INTO Demand (date, time, id_client, id_clerk) VALUES (%s, %s, %s, %s)'
DELETE_DEMAND = 'DELETE FROM Demand WHERE id = %s'
SEARCH_DEMAND = 'SELECT * FROM Product WHERE id_client = %s'
SEARCH_DEMAND = 'SELECT * FROM Product WHERE code = %s'
LISTING_DEMAND = 'SELECT d.id,d.date,d.time,c.name,k.name FROM Demand d JOIN Client c ON c.id_user = d.id_client ' \
                 'JOIN Clerk k ON k.id_user = d.id_clerk'
LISTING_DEMAND_OF_CLIENT = 'SELECT d.id,d.date,d.time,c.name,k.name FROM Demand d JOIN Client c ON c.id_user = d.id_client ' \
                           'JOIN Clerk k ON k.id_user = d.id_clerk WHERE c.id_user  = %(id)s'

SAVE_ITEM = 'INSERT INTO Item (id_demand,id_product,quantity) VALUES (%s, %s, %s)'
DELETE_ITEM = 'DELETE FROM Item WHERE id_demand = %(id)s AND id_product = %s'
ALTER_ITEM = 'UPDATE Item SET quantity = %(quantity)s WHERE id_demand = %(demand)s AND id_product = %(product)s'
SEARCH_ITEM = 'SELECT * FROM Item WHERE id_demand = %s AND id_product  = %s'
LISTING_ITEM = 'SELECT * FROM Item'


class DemandDAO(object):

    def __init__(self, connection):
        self.__connection = connection

    def save(self, demand):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(SAVE_DEMAND, (demand.date, demand.time, demand.id_client, demand.id_clerk))
        demand.id = cursor.lastrowid
        itemdao = ItemDAO(self.__connection)
        for item in demand.items:
            item.id_demand = demand.id
            itemdao.save(item)
        del (itemdao)
        self.__connection.confirm_transaction()
        return demand

    def delete(self, id):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(DELETE_DEMAND, {'id': id})
        self.__connection.confirm_transaction()

    def search(self, id):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(SEARCH_DEMAND, {'id': id})
        tuple = cursor.fetchall()
        return Demand(tuple[1], tuple[2], tuple[3], tuple[4], id=tuple[0])

    def search_demand_of_client(self, id):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(LISTING_DEMAND_OF_CLIENT, {'id': id})
        return self.__tuple_to_demands(cursor.fetchall())

    def show_all(self):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(LISTING_DEMAND)
        return self.__tuple_to_demands(cursor.fetchall())

    def __tuple_to_demands(self, tuples):
        def __map_tuple_to_object(tuple):
            return Demand(tuple[1], tuple[2], tuple[3], tuple[4],items=None, id=tuple[0])

        return list(map(__map_tuple_to_object, tuples))


class ItemDAO(object):

    def __init__(self, connection):
        self.__connection = connection

    def save(self, item):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(SAVE_ITEM, (item.id_demand, item.id_product, item.quantity))

    def delete(self, id):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(DELETE_ITEM, {'id': id})

    def alter(self, item):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(ALTER_ITEM, {'quantity': item.quantity, 'demand': item.id_demand, 'product': item.id_product})
        self.__connection.confirm_transaction()
        return item

    def search(self, id_demand, id_product):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(SEARCH_ITEM, (id_demand, id_product))
        tuple = cursor.fetchone()
        return Item(tuple[1], tuple[2], tuple[3])

    def show_all(self):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(LISTING_ITEM)
        products = self.__tuple_to_items(cursor.fetchall())
        return products

    def __tuple_to_items(self, tuples):
        def __map_tuple_to_object(tuple):
            return Item(tuple[1], tuple[2], tuple[3])

        return list(map(__map_tuple_to_object, tuples))
