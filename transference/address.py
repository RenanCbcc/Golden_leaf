class Address(object):
    def __init__(self,id,id_user,place,number,zip_code):
        self.__id = id
        self.__id_user = id_user
        self.__place = place
        self.__number = number
        self.__zip_code = zip_code

    @property
    def id(self):
        return self.__id

    @property
    def id_user(self):
        return self.__id_user

    @property
    def place(self):
        return self.__place

    @place.setter
    def place(self, string):
        self.__place = string

    @property
    def number(self):
        return self.__number

    @number.setter
    def number(self, number):
        self.__number = number

    @property
    def zip_code(self):
        return self.__zip_code

    @zip_code.setter
    def zip_code(self, string):
        self.__zip_code = string

    def __str__(self):
        return "Id_User: {}, Rua: {}, {}".format(self.__id_user,
                                                 self.__street,
                                                 self.__number)


class Phone(object):
    def __init__(self, identification, phone_number, notification):
        self.__identification = identification
        self.__notification = notification
        self.__phone_number = phone_number

    @property
    def phone_number(self):
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, number):
        self.__phone_number = number

    @property
    def identification(self):
        return self.__identification

    @property
    def notification(self):
        return self.__notification

    @notification.setter
    def notification(self, boolean):
        self.__notification = boolean

    def __str__(self):
        return "Usuário: {}, Número: {}, Notificação: {}".format(self.__id_user,
                                                                self.__phone_number,
                                                                self.__notification)

