from flask import request, session, redirect, url_for, render_template, flash, send_from_directory, Markup, jsonify
from app import app,db,bcrypt
from app.model import User,Item,Cart
from app.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

# def products(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, "products.html", context)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('customer/menu.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/order',methods=['GET','POST'])
def order():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Delivery':
            print("nar")
        elif request.form['submit_button'] == 'Pick-up':
            pass # do something else
        elif request.form['submit_button'] == 'Pick-up':
            print("fuck")
        else:
            pass # unknown
    elif request.method == 'GET':
        return render_template('customer/order.html')


@app.route('/cart')
def cart():
    return render_template('customer/cart.html')

@app.route('/checkout')
def checkout():
    return render_template('customer/checkout.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()#one or none
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('customer/login.html', title='Login', form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data,last_name=form.last_name.data,email=form.email.data, password=hashed_password)
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

@app.route('/order/create')
@login_required
def create_order():
    new_item = Item(name="water",description="wayer",cost=12.99)
    db.session.add(new_item)
    items = Item.query.all()
    print(items)
    return render_template('customer/create-order.html', title='Create an Order', items = items)

@app.route('/order/create')
@login_required
def guest_create_order():
    return render_template('customer/create-order.html', title='Create an Order')


@app.route('/staff-portal')
def staff():
    #ask to sign in
    return render_template('staff/staff-portal.html')


@app.route("/addToCart/<int:productId>")
@login_required
def addToCart(productId):
    #print(productId)
    # Using Flask-SQLAlchmy SubQuery
    if Cart.query.filter(Cart.userid == current_user.id).filter(Cart.productid == productId).one_or_none():
        cart_with_item = Cart.query.filter(Cart.userid == current_user.id).filter(Cart.productid == productId).one_or_none()
        print(cart_with_item.quantity)
        cart_with_item.quantity = cart_with_item.quantity + 1
        print(cart_with_item.quantity)
        db.session.merge(cart_with_item)
        db.session.flush()
        db.session.commit()
    else:
        cart = Cart(userid=current_user.id, productid=productId, quantity=1)
        db.session.merge(cart)
        db.session.flush()
        db.session.commit()
        print("new cart")


    print(current_user)
    # Using Flask-SQLAlchmy normal query
    # extractAndPersistKartDetailsUsingkwargs(productId)
    flash('Item successfully added to cart !!', 'success')
    return redirect(url_for('cart'))

def extractAndPersistKartDetailsUsingSubquery(productId):
    userId = User.query.with_entities(User.id).first()
    userId = userId[0]

    subqury = (Cart.userid == userId).filter(Cart.productid == productId).subquery()
    qry = db.session.query(Cart.quantity).select_entity_from(subqury).all()

    