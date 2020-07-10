from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask (__name__)
app.config['SECRET_KEY'] = 'd2a0e39be0acfb1a5e1781d37917dd18'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ffegiqyd:xaVHfoHDT4teo35dBBphCax8djyaTKro@ruby.db.elephantsql.com:5432/ffegiqyd'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
scheduler = BackgroundScheduler()

from webcheck import routes