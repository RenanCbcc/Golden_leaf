from manager import db


class Address(db.Model):
    __tablename__ = 'Addresses'
    id = db.Column(db.Integer, primary_key=True)
    place = db.Column(db.String(64))
    number = db.Column(db.SmallInteger)
    title = db.Column(db.String(64))
    zip_code = db.Column(db.String(6))
    client_id = db.Column(db.Integer, db.ForeignKey('client_id'))

    def __str__(self):
        return "Rua: {}, {}".format(self.place, self.number)


class Phone(db.Model):
    __tablename__ = 'phones'
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(64))
    notifiable = db.Column(db.Boolean)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return "Número: {}, Notificação: {}".format(self.phone_number,
                                                    self.notification)
