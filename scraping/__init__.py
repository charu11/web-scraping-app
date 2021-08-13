from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine
import pandas as pd

# initiate the flask app
app = Flask(__name__)

# initiate the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scraping.db'
app.config['SECRET_KEY'] = 'b36572e91cc4fd12ea88e36f'
db = SQLAlchemy(app)

# initiate sqlalchemy engine
engine = create_engine('sqlite:///scraping.db')

# initiate bcrypt
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = 'info'

from scraping import routes
