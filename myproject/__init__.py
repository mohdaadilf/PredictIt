# NECESSARY IMPORTS FOR SETTING UP FLASK AND USER AUTH
from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail, Message


# SETTING UP LOGIN MANAGER AND FLASK APP
login_manager = LoginManager()
app = Flask(__name__)

# CREATING THE DATABASE CONFIGS
app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data.sqlite')
print(os.path.join(basedir, 'data.sqlite'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#Email Initialization
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'predict.it.website@gmail.com'
app.config['MAIL_PASSWORD'] = 'marilynaadil'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# DATABASE CREATED AND MIGRATE SET UP
db = SQLAlchemy(app)
Migrate(app, db)

# INITIALIZING LOGIN MANAGER
login_manager.init_app(app)

# WHICH FUNCTION WILL THE USER NEED TO SEE FOR LOGIN
login_manager.login_view = "login"
