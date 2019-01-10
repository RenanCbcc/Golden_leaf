from manager import db


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    name = db.Column(db.String(64))
    price = db.Column(db.SmallInteger)
    is_available = db.Column(db.Boolean)
    code = db.Column(db.String(64))

    def __repr__(self):
        return '<Role %r>' % self.name

    def __eq__(self, other):
        return self.__code == other.__code
