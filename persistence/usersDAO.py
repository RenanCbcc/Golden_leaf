from transference.users import User,Client,Clerk

SAVE_USER = 'INSERT INTO User (name, cpf) VALUES(%s,%s)'
SAVE_CLIENT = 'INSERT INTO Client (id,surname, status) VALUES(%d,%s,%d)'
SAVE_CLERK = 'INSERT INTO Clerk (id, email, password) VALUES(%d,%s,%s)'
SEARCH_CLIENT= 'SELECT u.id,u.name,c.surname,u.cpf,c.status from User u, Client c where u.id = c.id'
SEARCH_CLERK= 'SELECT u.id,u.name,c.email,u.cpf,c.password from User u JOIN Clerk c on u.id = c.id'
DELETE_USER= 'DELETE Client WHERE USER.id = %d'
DELETE_CLIENT='DELETE Client WHERE Client.id = %d'
DELETE_CLERK= 'DELETE Client WHERE CLERK.id = %d'
UPDATE_USER='UPDATE User SET name=%s WHERE id = %d'
UPDATE_CLIENT='UPDATE User SET surname=%s, status=%d WHERE id = %d'
UPDATE_CLERK='UPDATE User SET email=%s, password=%s WHERE id = %d'
LISTING_CLIENT='SELECT u.id,u.name,c.surname,u.cpf,c.status FROM User u, Client c WHERE u.id = c.id'
LISTING_CLERK='SELECT u.id,u.name,u.cpf,c.email FROM User u, Clerk c WHERE u.id = c.id'

class ClientDAO(object):
    def __init__(self,connection):
        self.__connection = connection

    def save(self,client):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(SAVE_USER, (client.name,client.identification))
        client.id = cursor.lastrowid
        cursor.execute(SAVE_CLIENT, (client.id,client.surname,client.status))
        self.____connection.confirm_transaction()
        return client


    def search(self,id):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(SEARCH_CLIENT,(id))
        tuple = cursor.fetchone()
        return Client(tuple[0],tuple[1], tuple[2], tuple[3],tuple[4])

    def delete(self,id):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(DELETE_CLIENT,(id))
        cursor.execute(DELETE_USER,(id))
        self.____connection.confirm_transaction()

    def alter(self,client):
        cursor = self.__connection.get_connection().cursor()
        cursor.execute(UPDATE_USER, (client.name))
        cursor.execute(UPDATE_USER, (client.surname,client.status))
        self.____connection.confirm_transaction()


    def show(self):
        cursor = self.__connection.get_connection().cursor()
        clients = self.__listing(cursor.fetchall())
        return clients

    def __listing(tupla):
        return Jogo(tupla[1], tupla[2], tupla[3], id=tupla[0])

        return list(map(cria_jogo_com_tupla, jogos))


class ClerkDAO(object):
    pass






