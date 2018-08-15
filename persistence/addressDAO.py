from transference.addresses import Address, Phone

SAVE_ADDRESS = 'INSERT INTO Address (id_client,public_place,number,zip_code) values (%s, %s, %s, %s)'
DELETE_ADDRESS = 'DELETE FROM Address WHERE id_user = %(id_user)s'
ALTER_ADDRESS = 'UPDATE Address SET place = %s, number = %s, zip_code = %s WHERE id_user = $s'
SEARCH_ADDRESS = 'SELECT c.name,a.public_place,a.number, a.zip_code FROM Address a JOIN Client c ' \
                 'ON a.id_client = c.id_user WHERE id_user = %(id_user)s'
LISTING_ADDRESS = 'SELECT c.name,a.public_place,a.number, a.zip_code FROM Address a JOIN Client c ' \
                  'ON a.id_client = c.id_user'

SAVE_PHONE = 'INSERT INTO Phone (id_user, phone_number, notification) values (%s, %s, %s)'
DELETE_PHONE = 'DELETE FROM Phone WHERE id_user = %s'
UPDATE_PHONE = 'UPDATE Phone SET phone_number = %s, notification = %s WHERE id_user = %s'
SEARCH_PHONE = 'SELECT * FROM Phone p WHERE p.id_user = %(id_user)s'


class AddressDAO(object):

    def __init__(self, connection):
        self.__connection = connection

    def save(self, address):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(SAVE_ADDRESS, (address.id_client, address.place, address.number, address.zip_code))
        self.__connection.confirm_transaction()
        return address

    def delete(self, id_user):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(DELETE_ADDRESS, (id_user,))
        self.__connection.confirm_transaction()

    def alter(self, address):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(ALTER_ADDRESS, (address.place, address.number, address.zip_code, address.id_user))
        self.__connection.confirm_transaction()
        return address

    def search(self, id_user):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(SEARCH_ADDRESS, {'id_user': id_user})
        tuple = cursor.fetchone()
        return Address(tuple[0], tuple[1], tuple[2], tuple[3])

    def show_all(self):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(LISTING_ADDRESS)
        clerks = self.__tuple_to_addesses(cursor.fetchall())
        return clerks

    def __tuple_to_addesses(self, tuples):
        def __map_tuple_to_object(tuple):
            return Address(tuple[0], tuple[1], tuple[2], tuple[3], tuple[4])

        return list(map(__map_tuple_to_object, tuples))


class PhoneDAO(object):

    def __init__(self, connection):
        self.__connection = connection

    def save(self, phone):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(SAVE_PHONE, (phone.id_user, phone.phone_number, phone.notification))
        self.__connection.confirm_transaction()
        return phone

    def delete(self, id_user):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(DELETE_PHONE, {'id_user': id_user})
        self.__connection.confirm_transaction()

    def alter(self, phone):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(UPDATE_PHONE, (phone.phone_number, phone.notification, phone.id_user))
        self.__connection.confirm_transaction()
        return phone

    def search(self, id_user):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(SEARCH_PHONE, {'id_user': id_user})
        tuple = cursor.fetchone()
        return Phone(tuple[0], tuple[1], tuple[2])
