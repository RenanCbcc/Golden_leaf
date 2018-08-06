from transference.users import Client, Clerk

SAVE_USER = 'INSERT INTO User (cpf,status) VALUES(%s,%s)'
SAVE_CLIENT = 'INSERT INTO Client (id_user,name,surname) VALUES(%s,%s,%s)'
SAVE_CLERK = 'INSERT INTO Clerk (id_user,name,email,password) VALUES(%s,%s,%s,%s)'
SEARCH_CLIENT = 'SELECT u.id,c.name,c.surname,u.cpf,u.status FROM User u JOIN Client c on u.id = c.id_user ' \
                'WHERE u.id = %(id)s'
SEARCH_CLERK = 'SELECT u.id,c.name,c.email,c.password,u.cpf,u.status FROM User u JOIN Clerk c on u.id = c.id_user ' \
               'WHERE c.id_user = %(id)s'

SEARCH_CLIENT_FOR_NAME = 'SELECT u.id,c.name,c.surname,u.cpf,u.status FROM User u JOIN Client c on u.id = c.id_user ' \
                         'WHERE c.name LIKE %(name)s%'
SEARCH_CLERK_FOR_EMAIL = 'SELECT u.id,c.name,c.email,c.password,u.cpf,u.status FROM User u JOIN Clerk c on u.id = c.id_user ' \
                         'WHERE c.email = %(email)s'
DELETE_USER = 'DELETE Client WHERE USER.id = %s'
DELETE_CLIENT = 'DELETE Client WHERE Client.id_user = %(id)s'
DELETE_CLERK = 'DELETE Clerk WHERE Clerk.id_user = %(id)s'
UPDATE_USER = 'UPDATE User SET status=%s WHERE id = %(id)s'
UPDATE_CLIENT = 'UPDATE Client SET name= %s, surname=%s WHERE id_user = %s'
UPDATE_CLERK = 'UPDATE Clerk SET name= %s, email=%s, password=%s WHERE id_user = %s'
LISTING_CLIENT = 'SELECT u.id,c.name,c.surname,u.cpf,u.status FROM User u JOIN Client c on u.id = c.id_user'
LISTING_CLERK = 'SELECT u.id,c.name,c.email,u.cpf,u.status FROM User u JOIN Clerk c on u.id = c.id_user'


class ClientDAO(object):
    def __init__(self, connection):
        self.__connection = connection

    def save(self, client):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(SAVE_USER, (client.identification, client.status))
        client.id = cursor.lastrowid
        cursor.execute(SAVE_CLIENT, (client.id, client.name, client.surname))
        self.__connection.confirm_transaction()
        return client

    def search(self, id):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(SEARCH_CLIENT, {'id': id})
        tuple = cursor.fetchone()
        "Client(name, surname, identification,status=True, id=0):"
        return Client(tuple[1], tuple[2], tuple[3], status=tuple[4], id=tuple[0])

    def search_for_name(self, name):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(SEARCH_CLIENT_FOR_NAME, {'name': name})
        tuple = cursor.fetchall()
        "Client(name, surname, identification,status=True, id=0):"
        return Client(tuple[1], tuple[2], tuple[3], status=tuple[4], id=tuple[0])

    def delete(self, id):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(DELETE_CLIENT, {'id': id})
        cursor.execute(DELETE_USER, {'id': id})
        self.__connection.confirm_transaction()

    def alter(self, client):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(UPDATE_USER, (client.status, client.id))
        cursor.execute(UPDATE_CLIENT, (client.name, client.surname, client.id))
        self.__connection.confirm_transaction()
        return client

    def show_all(self):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(LISTING_CLIENT)
        clients = self.__tuple_to_client(cursor.fetchall())
        return clients

    def __tuple_to_client(self, clients):
        def __map_tuple_to_object(tuple):
            return Client(tuple[1], tuple[2], tuple[3], status=tuple[4], id=tuple[0])

        return list(map(__map_tuple_to_object, clients))


class ClerkDAO(object):
    def __init__(self, connection):
        self.__connection = connection

    def save(self, clerk):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(SAVE_USER, (clerk.identification, clerk.status))
        clerk.id = cursor.lastrowid
        cursor.execute(SAVE_CLERK, (clerk.id, clerk.name, clerk.email, clerk.password))
        self.__connection.confirm_transaction()
        return clerk

    def search(self, id):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(SEARCH_CLERK, {'id': id})
        tuple = cursor.fetchone()
        "Clerk(name,email,password,identification,status=True,id=0)"
        return Clerk(tuple[1], tuple[2], tuple[3], tuple[4], status=tuple[5], id=tuple[0])

    def delete(self, id):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(DELETE_CLERK, {'id': id})
        cursor.execute(DELETE_USER, {'id': id})
        self.__connection.confirm_transaction()

    def alter(self, clerk):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(UPDATE_USER, (clerk.status, clerk.id))
        cursor.execute(UPDATE_CLERK, (clerk.name, clerk.email, clerk.password, clerk.id))
        self.__connection.confirm_transaction()
        return clerk

    def login(self, email):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(SEARCH_CLERK_FOR_EMAIL, (email,))
        tuple = cursor.fetchone()
        "Clerk(name,email,password,identification,status=True,id=0)"
        return Clerk(tuple[1], tuple[2], tuple[3], tuple[4], status=tuple[5], id=tuple[0])

    def show_all(self):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(LISTING_CLERK)
        clerks = self.__tuple_to_clerks(cursor.fetchall())
        return clerks

    def __tuple_to_clerks(self, clerks):
        def __map_tuple_to_object(tuple):
            return Client(tuple[1], tuple[2], tuple[3], status=tuple[4], id=tuple[0])

        return list(map(__map_tuple_to_object, clerks))
