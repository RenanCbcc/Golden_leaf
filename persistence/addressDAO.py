from transference.address import Address

SAVE_ADDRESS = 'INSERT INTO Address (id_user,place,number,zip_code) values (%d, %s, %s, %s)'
DELETE_ADDRESS = 'DELETE FROM Address WHERE id_user = ?'
ALTER_ADDRESS = 'UPDATE Address SET place = ?, SET number = ?, SET zip_code = ? WHERE id_user = ?'
SEARCH_ADDRESS = 'SELECT u.name,c.surname,a.public_place,a.zip_code,c.status FROM User u ' \
                 'JOIN Client c ON u.id = c.id JOIN Address a on u.id = a.id_client ' \
                 'WHERE u.id = %d'

LISTING_ADDRESS='SELECT u.name,c.surname,a.public_place,a.zip_code,c.status FROM User u ' \
                'JOIN Client c ON u.id = c.id JOIN Address a on u.id = a.id_client'


class AddressDAO(object):

    def __init__(self, connection):
        self.__connection = connection

    def save(self, address):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(SAVE_ADDRESS, (address.id_user, address.place, address.number, address.zip_code))
        self.____connection.confirm_transaction()
        return address

    def delete(self, id_user):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(DELETE_ADDRESS, (id_user))
        self.__connection.confirm_transaction()

    def alter(self, address):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(ALTER_ADDRESS, (address.place, address.number, address.zip_code))
        self.__connection.confirm_transaction()
        return address

    def search(self, id_user):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(SEARCH_ADDRESS, (id_user))
        tuple = cursor.fetchone()
        return Address(tuple[0],tuple[1], tuple[2], tuple[3],tuple[4])

    def show_all(self):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(LISTING_ADDRESS)
        clerks = self.__tuple_to_addesses(cursor.fetchall())
        return clerks

    def __tuple_to_addesses(self, address):
        def __map_tuple_to_object(tuple):
            return Address(tuple[0], tuple[1], tuple[2], tuple[3],tuple[4])

        return list(map(__map_tuple_to_object,address))


