import MySQLdb
import MySQLdb.cursors as cursors


class Connection(object):

    def __init__(self):
        self.__connection = MySQLdb.connect(user='flask',
                                            password='showmethemoney',
                                            database='commerce',
                                            host='localhost',
                                            port=3306, cursorclass=cursors.SSCursor)

    def get_connection(self):
        return self.__connection

    def close_connection(self):
        if not self.__connection.open or self.__connection is None:
            return
        else:
            self.__connection.close()

    def confirm_transaction(self):
        if not self.__connection.open or self.__connection is None:
            return
        else:
            self.__connection.commit()


