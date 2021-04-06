from flask import request, session, redirect, url_for, render_template, flash, send_from_directory, Markup, jsonify
from app import app, db, bcrypt
from app.model import User, Item, Cart, Order
from app.forms import RegistrationForm, LoginForm, CheckoutForm
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime

# def products(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, "products.html", context)

# instead of calculating the number of items at each iinstance where we use
# the base template, we can create a varible
# that is accessible by all requests
# render_template('customer/menu.html',items=items)
# render_template('customer/menu.html',items=items, len carts)


@app.context_processor
def inject_cart():
    if current_user.is_authenticated:
        uid = current_user.id
        carts = Cart.query.filter_by(userid=uid).all()
        carts = len(carts)
        return dict(len_carts=carts)
    return dict(len_carts=0)


@app.route('/order-history')
def order_history():
    # get orders from user in array and then iterate over them
    return render_template('customer/order_history.html')


@app.route('/saved_cards')
def saved_cards():
    # get orders from user in array and then iterate over them
    return render_template('customer/saved_cards.html')


@app.route('/saved_addresses')
def saved_addresses():
    # get orders from user in array and then iterate over them
    return render_template('customer/saved_addresses.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/menu')
def menu():
    items = Item.query.all()
    return render_template('customer/menu.html', items=items)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/order')
def order():
    items = Item.query.all()
    return render_template('customer/order.html', title='Create an Order', items=items)


@app.route('/payment', methods=['GET', 'POST'])
def payment():
    return render_template('customer/payment.html')


@app.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    form = CheckoutForm()

    if request.method == 'GET':
        if current_user.is_authenticated:
            uid = current_user.id
            carts = Cart.query.filter_by(userid=uid).all()
            items = []
            total = 0
            for cart in carts:
                item = Item.query.filter_by(id=cart.productid).first()
                items.append(item)
                total = total + item.cost
        return render_template('customer/cart.html', items=items, total=total, form=form)

    if request.method == 'POST':
        if current_user.is_authenticated:
            uid = current_user.id
            carts = Cart.query.filter_by(userid=uid).all()
            form_data = request.values.copy()
            for key, value in request.form.items():
                print("key: {0}, value: {1}".format(key, value))

            if form.validate_on_submit():
                total = 0
                for cart in carts:
                    item = Item.query.filter_by(id=cart.productid).first()
                    total += item.cost
                # fix this line by adding uiud
                #order = Order(orderid=,order_date=datetime.utcnow(),
                              total_price=total, userid=uid)
                db.session.add(order)
                db.session.commit()

                flash(f'Order Created for {form.full_name.data}!', 'success')
                return redirect(url_for('payment'))
            else:
                flash('Order not created.', 'danger')
                return redirect(url_for('cart'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            email=form.email.data).first()  # one or none
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('customer/login.html', title='Login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data, last_name=form.last_name.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.first_name.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('customer/register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/account')
@login_required
def account():
    return render_template('customer/account.html', title='Account')


@app.route('/staff-portal')
def staff():
    # ask to sign in
    return render_template('staff/staff-portal.html')


@app.route("/addToCart/<int:productId>")
@login_required
def addToCart(productId):
    # Using Flask-SQLAlchmy SubQuery
    if Cart.query.filter(Cart.userid == current_user.id).filter(Cart.productid == productId).one_or_none():
        cart_with_item = Cart.query.filter(Cart.userid == current_user.id).filter(
            Cart.productid == productId).one_or_none()
        cart_with_item.quantity = cart_with_item.quantity + 1
        db.session.merge(cart_with_item)
        db.session.flush()
        db.session.commit()
    else:
        cart = Cart(userid=current_user.id, productid=productId, quantity=1)
        db.session.merge(cart)
        db.session.flush()
        db.session.commit()

    # Using Flask-SQLAlchmy normal query
    # extractAndPersistKartDetailsUsingkwargs(productId)
    flash('Item successfully added to cart !!', 'success')
    return redirect(url_for('order'))


@app.route("/removeItem/<int:productId>")
@login_required
def removeItem(productId):
    # Using Flask-SQLAlchmy SubQuery
    if Cart.query.filter(Cart.userid == current_user.id).filter(Cart.productid == productId).one_or_none():
        Cart.query.filter(Cart.userid == current_user.id).filter(
            Cart.productid == productId).delete()
        db.session.commit()
    else:
        flash('Item not in cart', 'error')
        return redirect(url_for('cart'))

    # Using Flask-SQLAlchmy normal query
    # extractAndPersistKartDetailsUsingkwargs(productId)
    flash('Item removed from cart !!', 'success')
    return redirect(url_for('cart'))
