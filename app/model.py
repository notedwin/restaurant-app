from app import db, login_manager
from flask_login import UserMixin
from slugify import slugify
from sqlalchemy import event


ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(20))# unique=True) # nullable=False,
    password = db.Column(db.String(60), nullable=False)
    points = db.Column(db.Integer, nullable=True, default=0)
    #addresses = db.relationship('Address', backref='user', lazy=True)
    #stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}')"

class Address(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    street_address = db.Column(db.String(120), nullable=False)
    country = db.Column(db.String(120), nullable=False)
    zip = db.Column(db.Integer,nullable=False)
    default = db.Column(db.Boolean,default=False)
    #person_id = db.Column(db.Integer, db.ForeignKey('person.id'),nullable=False)

class Item(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(), nullable=True)
    cost = db.Column(db.Numeric, nullable=False)

    def __repr__(self):
        return f"Item('{self.id}', '{self.name}', '{self.cost}')"
class Cart(db.Model):
    __table_args__ = {'extend_existing': True}
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    productid = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Cart('{self.userid}', '{self.productid}', '{self.quantity}')"

class Order(db.Model):
    __table_args__ = {'extend_existing': True}
    orderid = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, nullable=False)
    total_price = db.Column(db.DECIMAL, nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)

class OrderedProduct(db.Model):
    __table_args__ = {'extend_existing': True}
    ordproductid = db.Column(db.Integer, primary_key=True)
    orderid = db.Column(db.Integer,db.ForeignKey('order.orderid'), nullable=False)
    productid = db.Column(db.Integer,db.ForeignKey('item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)