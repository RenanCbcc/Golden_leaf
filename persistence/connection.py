import MySQLdb
import MySQLdb.cursors as cursors


class Connection(object):
    def __init__(self):
        self.__connection = MySQLdb.connect(user='root',
                                            password='admin',
                                            database='commerce',
                                            host='localhost',
                                            port=3306, cursorclass=cursors.SSCursor)

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
