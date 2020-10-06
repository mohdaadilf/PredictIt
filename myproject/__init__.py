# NECESSARY IMPORTS FOR SETTING UP FLASK AND USER AUTH
from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# SETTING UP LOGIN MANAGER AND FLASK APP
login_manager = LoginManager()
app = Flask(__name__)

# CREATING THE DATABASE CONFIGS
app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# DATABASE CREATED AND MIGRATE SET UP
db = SQLAlchemy(app)
Migrate(app, db)

# iNITIALIZING LOGIN MANAGER
login_manager.init_app(app)

# WHICH FUNCTION WILL THE USER NEED TO SEE FOR LOGIN
login_manager.login_view = "login"
