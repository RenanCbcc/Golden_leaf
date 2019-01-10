from manager import db


class Address(db.Model):
    __tablename__ = 'Addresses'
    __place = db.Column(db.String(64))
    __number = db.Column(db.SmallInteger)
    __zip_code = db.Column(db.String(6))
    __client_id = db.Column(db.Integer, db.ForeignKey('client_id'))

    def __init__(self, id_client, place, number, zip_code):
        self.__client_id = id_client
        self.__place = place
        self.__number = number
        self.__zip_code = zip_code

    @property
    def id_client(self):
        return self.__client_id

    @property
    def place(self):
        return self.place

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
        return "Rua: {}, {}".format(self.__place, self.__number)


class Phone(db.Model):
    __tablename__ = 'telephones'
    __id = db.Column(db.Integer, primary_key=True)
    __phone_number = db.Column(db.String(64))
    __notifiable = db.Column(db.Boolean)
    __member_id = db.Column(db.Integer, db.ForeignKey('member_id'))

    def __init__(self, member_id, phone_number, notifiable):
        self.__member_id = member_id
        self.__notifiable = notifiable
        self.__phone_number = phone_number

    @property
    def phone_number(self):
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, number):
        self.__phone_number = number

    @property
    def member_id(self):
        return self.__member_id

    @property
    def notifiable(self):
        return self.__notifiable

    @notifiable.setter
    def notifiable(self, boolean):
        self.__notifiable = boolean

    def __repr__(self):
        return "Número: {}, Notificação: {}".format(self.__phone_number,
                                                    self.__notifiable)
