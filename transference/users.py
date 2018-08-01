class User(object):
    def __init__(self, id, name, identification):
        self.__id = id
        self.__name = name
        self.__identification = identification

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, string):
        self.__name = string

    @property
    def identification(self):
        return self.__identification


class Client(User):
    def __init__(self,id, name,surname,identification,status):
        super().__init__(id,name,identification)
        self.__id = id
        self.__surname = surname
        self.__status = status

    @property
    def surname(self):
        return self.__surname

    @surname.setter
    def surname(self, string):
        self.__surname = string

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, boolean):
        self.__status = boolean

    def __str__(self):
        return "Cliente: {} {}, CPF: {}".format(super().name,
                                                       self.__surname,
                                                       super().identification
                                                     )


class Clerk(User):
    def __init__(self, id, name,identification, email, password):
        super().__init__(id, name, identification)
        self.__email = email
        self.__password = password

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, string):
        self.__email = string

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, string):
        self.__password = string

    def __str__(self):
        return "Atendente: {}, Email: {}, CPF: {}".format(super().name,
                                               self.__email,
                                               super().identification
                                                     )
