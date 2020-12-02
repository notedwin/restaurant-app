
from app import app,db
from app.model import User,Item,Cart

Cart.query.delete()
Item.query.delete()

new_item = Item(name="small mushroom pizza",description="pizza with mushrooms",cost=8.99)
db.session.add(new_item)
new_item = Item(name="medium mushroom pizza",description="pizza with mushrooms",cost=12.99)
db.session.add(new_item)
new_item = Item(name="large mushroom pizza",description="pizza with mushrooms",cost=16.99)
db.session.add(new_item)

new_item = Item(name="small peperonni pizza",description="pizza with peperonnis",cost=8.99)
db.session.add(new_item)
new_item = Item(name="medium peperonni pizza",description="pizza with peperonnis",cost=12.99)
db.session.add(new_item)
new_item = Item(name="large peperonni pizza",description="pizza with peperonnis",cost=16.99)
db.session.add(new_item)

new_item = Item(name="small cheese pizza",description="pizza with cheese",cost=8.99)
db.session.add(new_item)
new_item = Item(name="medium cheese pizza",description="pizza with cheese",cost=12.99)
db.session.add(new_item)
new_item = Item(name="large cheese pizza",description="pizza with cheese",cost=16.99)
db.session.add(new_item)


db.session.commit()
