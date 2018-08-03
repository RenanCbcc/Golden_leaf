from transference.address import Address

SAVE_ADDRESS = 'INSERT INTO Address (id_client,public_place,number,zip_code) values (%s, %s, %s, %s)'
DELETE_ADDRESS = 'DELETE FROM Address WHERE id_user = %(id_user)s'
ALTER_ADDRESS = 'UPDATE Address SET place = %s, number = %s, zip_code = %s WHERE id_user = $s'
SEARCH_ADDRESS = 'SELECT c.name,a.public_place,a.zip_code,u.status FROM User u JOIN Client c ' \
                 'ON u.id = c.id_user JOIN Address a on u.id = %(id_user)s'

LISTING_ADDRESS = 'SELECT c.name,a.public_place,a.zip_code,c.status FROM User u ' \
                  'JOIN Client c ON u.id = c.id JOIN Address a on u.id = a.id_client'

SAVE_PHONE = 'INSERT INTO Phone (id_cpf, phone_number, notification) values (%s, %s, %s)'
DELETE_PHONE = 'DELETE FROM Phone WHERE id_cpf = %s'
ALTER_PHONE = 'UPDATE Phone SET SET number = %s WHERE id_cpf = %s'
SEARCH_PHONE = 'SELECT p.phone_number FROM Phone p WHERE id_cpf = %s'


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
        print(tuple)
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
        cursor.execute(SAVE_ADDRESS, (phone.identification, phone.phone_number, phone.notification))
        self.__connection.confirm_transaction()
        return phone

    def delete(self, id_user):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(DELETE_ADDRESS,{'id_user': id_user})
        self.__connection.confirm_transaction()

    def alter(self, phone):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(ALTER_ADDRESS, (phone.identification, phone.phone_number, phone.notification))
        self.__connection.confirm_transaction()
        return phone

    def search(self, identification):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(SEARCH_ADDRESS, (identification))
        tuple = cursor.fetchone()
        return Address(tuple[0], tuple[1], tuple[2])
