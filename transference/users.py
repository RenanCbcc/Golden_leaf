class User(object):
    def __init__(self,identification,status):
        self.__identification = identification
        self.__status = status

    @property
    def identification(self):
        return self.__identification

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, boolean):
        self.__status = boolean

    def __str__(self):
        return "Usuário: {}, CPF: {}".format(self.__identification,self.__status)


class Client(User):
    def __init__(self,name,surname,identification,status):
        super().__init__(identification,status)
        self.__name = name
        self.__surname = surname
        self.__id = None

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self,value):
        self.__id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, string):
        self.__name = string

    @property
    def surname(self):
        return self.__surname

    @surname.setter
    def surname(self, string):
        self.__surname = string


    def __str__(self):
        return "Cliente: {} {}, CPF: {}".format(super().name,self.__surname)


class Clerk(User):
    def __init__(self,name,identification, email, password,status):
        super().__init__(identification,status)
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
        return "Atendente: {}, Email: {}".format(self.__name,self.__email)
