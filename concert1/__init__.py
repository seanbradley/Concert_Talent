# -*- coding: utf-8 -*-

import os, datetime
from flask import Flask, render_template
#from flask_mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, UserMixin, RoleMixin, login_required
from flask.ext.security.datastore.sqlalchemy import SQLAlchemyUserDatastore
from concert1.security import security
from concert1.base import base

#FLASK_APP_DIR = os.path.dirname(os.path.abspath(__file__))

# Create app
app = Flask(__name__)

# Config requires legit Gmail username and password
# Move eventually to config.py w/ diff config for production
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'sean@concerttalent.com'
app.config['MAIL_PASSWORD'] = 'password'
app.config['DEFAULT_MAIL_SENDER'] = 'Admin < sean@concerttalent.com >'
#mail = Mail(app)

# Create database connection object
db = SQLAlchemy(app)

'''
# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Create a user for testing purposes
@app.before_first_request
def create_user():
    db.create_all()
    user_datastore.create_user(email='sean@concerttalent.com', password='password')
    db.session.commit()
'''

class UserAccountMixin():
        first_name = db.Column(db.String(120))
        last_name = db.Column(db.String(120))

Security(app, SQLAlchemyUserDatastore(db, UserAccountMixin))

app.register_blueprint(security)
app.register_blueprint(base)


# Views
'''
@app.route('/google4fda8ef7d8ce7a73.html')
def google_webmaster_tools():
    return render_template('google4fda8ef7d8ce7a73.html')

@app.route('/')
@login_required
def home():
    return render_template('index.html', now=datetime.datetime.now)
'''


