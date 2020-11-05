from flask import Flask, request, session, redirect, url_for, render_template, flash, send_from_directory, Markup, jsonify
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome
from forms import LoginForm
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import RegistrationForm, LoginForm



app = Flask(__name__,static_url_path='/static',static_folder='static')
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
#app.config.from_pyfile('config.cfg')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False



Bootstrap(app)
FontAwesome(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/order',methods=['GET','POST'])
def order():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Do Something':
            pass # do something
        elif request.form['submit_button'] == 'Do Something Else':
            pass # do something else
        else:
            pass # unknown
    elif request.method == 'GET':
        return render_template('customer/order.html')


@app.route('/menu')
def menu():
    return render_template('customer/menu.html')

@app.route('/cart')
def cart():
    return render_template('customer/cart.html')

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('customer/login.html', title='Login', form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.first_name.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('customer/register.html', title='Register', form=form)

@app.route('/staff-portal')
def staff():
    #ask to sign in
    return render_template('staff/staff-portal.html')

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.run(debug=True)