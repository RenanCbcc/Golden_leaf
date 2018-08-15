from abc import ABCMeta


class User(object):
    __metaclass__ = ABCMeta

    def __init__(self, id, identification, status):
        self.__identification = identification
        self.__status = status
        self.__id = id

    @property
    def id(self):
        """
        :return: id
        """
        return self.__id

    @id.setter
    def id(self, value):
        """
        Sets an attribute
        :param value: id
        :return: void
        """
        self.__id = value

    @property
    def identification(self):
        """
        :return: identification
        """
        return self.__identification

    @property
    def status(self):
        """
        :return: status
        """
        return self.__status

    @status.setter
    def status(self, boolean):
        """
        :param boolean:
        :return: status
        """
        self.__status = boolean

    def __eq__(self, other):
        return self.id == other.id

    def __eq__(self, other):
        return self.identification == other.identification

    def __str__(self):
        """
        Return an informal representation of the class.
        :return: identification and status
        """
        return "CPF: {}, Status: {}".format(self.__identification, self.__status)


class Client(User):
    def __init__(self, name, surname, identification, status=True, id=0):
        super().__init__(id, identification, status)
        self.__name = name
        self.__surname = surname

    @property
    def name(self):
        """
        This method returns the name of the client as a string.
        :return: name
        """
        return self.__name

    @name.setter
    def name(self, string):
        """
        This method sets the name of the client.
        :param string: name
        :return:void
        """
        self.__name = string

    @property
    def surname(self):
        """
        This method returns the surname of the client as a string.
        :return: surname
        """
        return self.__surname

    @surname.setter
    def surname(self, string):
        self.__surname = string

    def __str__(self):
        """
        Return a informal representation of the class.
        :return: name and surname.
        """
        return "Cliente: {} {}".format(self.__name, self.__surname)


class Clerk(User):
    def __init__(self, name, email, password, identification, status=True, id=0):
        super().__init__(id, identification, status)
        self.__name = name
        self.__email = email
        self.__password = password

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, string):
        self.__name = string

    @property
    def email(self):
        """
        This method returns the email of the clerk as a string.
        :return: email
        """
        return self.__email

    @email.setter
    def email(self, string):
        """
        This method sets the email of the clerk.
        :param string: email
        :return: void
        """
        self.__email = string

    @property
    def password(self):
        """
        This method returns the password of the clerk as a string.
        :return: password
        """
        return self.__password

    @password.setter
    def password(self, string):
        """
        This method sets the password of the clerk.
        :param string: password
        :return: void
        """
        self.__password = string

    def __str__(self):
        """
        Return a informal representation of the class.
        :return: name and email.
        """
        return "Atendente: {}, Email: {}".format(self.__name, self.__email)
