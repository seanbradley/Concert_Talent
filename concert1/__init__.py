# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask.ext.mongoengine import MongoEngine
from flask.ext.security import (Security, UserMixin, RoleMixin, login_required,
    MongoEngineUserDatastore)

# Create app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'

# MongoDB Config
app.config['MONGODB_DB'] = 'concertdb'
app.config['MONGODB_HOST'] = 'localhost'
app.config['MONGODB_PORT'] = 27017

# Create database connection object
db = MongoEngine(app)

class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)

class User(db.Document, UserMixin):
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])

# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Create a user for testing
@app.before_first_request
def create_user():
    user_datastore.create_user(email='sean@concerttalent.com', password='password')

# Views
@app.route('/')
@login_required
def home():
    return render_template('index.html')