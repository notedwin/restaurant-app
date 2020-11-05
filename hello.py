from flask import Flask, request, session, redirect, url_for, render_template, flash, send_from_directory, Markup, jsonify
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome

app = Flask(__name__,static_url_path='/static',static_folder='static')
Bootstrap(app)
FontAwesome(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET' :
        return render_template('login.html')

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.run(debug=True)