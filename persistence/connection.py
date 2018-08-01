import MySQLdb

class Connection(object):
    def __init__(self):
        self.__connection = MySQLdb(user='root',
                                    password='admin',
                                    database='smart_vendinha',
                                    host='localhost',
                                    port=3306)

    def get_connection(self):
        return self.__connection

    def close_connection(self):
        if self.__connection.isClosed() or self.__connection is None:
            return
        else:
            self.__connection.cursos().closed()

    def confirm_transaction(self):
        if self.__connection.isClosed() or self.__connection is None:
            return
        else:
            self.__connection.cursos().commit()
