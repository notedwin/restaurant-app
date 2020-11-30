from flask import Flask
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome
import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_admin import Admin


app = Flask(__name__,static_url_path='/static',static_folder='static')
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI']  = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']  = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

#app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
#admin = Admin(app, name='microblog', template_mode='bootstrap4')
# Add administrative views here

from app import routes
#app.config.from_pyfile('config.cfg')

Bootstrap(app)
FontAwesome(app)
