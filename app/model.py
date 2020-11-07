from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}')"


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(), nullable=False)
    cost = db.Column(db.Numeric, nullable=False)

    def __repr__(self):
        return f"Item('{self.name}', '{self.cost}')"

#class Order(db.Model):