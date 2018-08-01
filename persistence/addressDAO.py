from transference.address import Address

SAVE_ADDRESS = 'INSERT INTO Address (id_user,place,number,zip_code) values (%d, %s, %s, %s)'
DELETE_ADDRESS = 'DELETE FROM Address WHERE id_user = ?'
ALTER_ADDRESS = 'UPDATE Address SET place = ?, SET number = ?, SET zip_code = ? WHERE id_user = ?'
SEARCH_ADDRESS = 'SELECT * FROM Address WHERE id_user = ?'


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
        return Address(tuple[1], tuple[2], tuple[3], id=tuple[0])
