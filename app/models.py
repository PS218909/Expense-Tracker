from . import db

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer)
    name = db.Column(db.String(50), nullable=False, primary_key=True)

class Expense(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), db.ForeignKey('categories.name'))
    date = db.Column(db.DateTime, default=db.func.current_timestamp())