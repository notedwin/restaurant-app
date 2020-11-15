from app import db, login_manager
from flask_login import UserMixin


ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    #stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}')"


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(), nullable=False)
    cost = db.Column(db.Numeric, nullable=False)
    #slug = models.SlugField()
    #image = models.ImageField()

    def __repr__(self):
        return f"Item('{self.name}', '{self.cost}')"

#   def get_absolute_url(self):
#       return reverse("core:product", kwargs={
#        'slug': self.slug
#    })
#
    #def get_add_to_cart_url(self):
    #    return reverse("core:add-to-cart", kwargs={
    #        'slug': self.slug
    #    })
#
    #def get_remove_from_cart_url(self):
    #    return reverse("core:remove-from-cart", kwargs={
    #        'slug': self.slug
    #    })

#class Order(db.Model):
#    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
#    items = models.ManyToManyField(OrderItem)
#    ordered_date = models.DateTimeField()
#    ordered = models.BooleanField(default=False)
#    shipping_address = models.ForeignKey( 'Address', related_name='shipping_address', #on_delete=models.SET_NULL, blank=True, null=True)
#    billing_address = models.ForeignKey('Address', related_name='billing_address', #on_delete=models.SET_NULL, blank=True, null=True)
#    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, #null=True)
#
#    def get_total(self):
#        total = 0
#        for order_item in self.items.all():
#            total += order_item.get_final_price()
#        return total

#class OrderItem(models.Model):
#    user = models.ForeignKey(settings.AUTH_USER_MODEL,
#                             on_delete=models.CASCADE)
#    ordered = models.BooleanField(default=False)
#    item = models.ForeignKey(Item, on_delete=models.CASCADE)
#    quantity = models.IntegerField(default=1)
#
#
#    def __str__(self):
#        return f"{self.quantity} of {self.item.productName}"
#
#    def get_total_item_price(self):
#        return self.quantity * self.item.price
#
#    def get_total_discount_item_price(self):
#        return self.quantity * self.item.discount_price
#
#    def get_amount_saved(self):
#        return self.get_total_item_price() - self.get_total_discount_item_price()
#
#    def get_final_price(self):
#        if self.item.discount_price:
#            return self.get_total_discount_item_price()
#        return self.get_total_item_price()
#

#
#class Address(models.Model):
#    user = models.ForeignKey(settings.AUTH_USER_MODEL,
#                             on_delete=models.CASCADE)
#    street_address = models.CharField(max_length=100)
#    apartment_address = models.CharField(max_length=100)
#    country = CountryField(multiple=False)
#    zip = models.CharField(max_length=100)
#    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
#    default = models.BooleanField(default=False)
#
#    def __str__(self):
#        return self.user.username
#
#    class Meta:
#        verbose_name_plural = 'Addresses'
#
#

#class Payment(models.Model):
#    stripe_charge_id = models.CharField(max_length=50)
#    user = models.ForeignKey(settings.AUTH_USER_MODEL,
#                             on_delete=models.SET_NULL, blank=True, null=True)
#    amount = models.FloatField()
#    timestamp = models.DateTimeField(auto_now_add=True)
#
#    def __str__(self):
#        return self.user.username
