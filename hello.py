from flask import Flask, request, session, redirect, url_for, render_template, flash, send_from_directory, Markup, jsonify
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome


app = Flask(__name__,static_url_path='/static',static_folder='static')
#app.config.from_pyfile('config.cfg')
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
    if request.method == 'GET' :
        return render_template('customer/login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET' :
        return render_template('customer/register.html')

@app.route('/staff-portal')
def staff():
    #ask to sign in
    return render_template('staff/staff-portal.html')

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.run(debug=True)