# -*- coding: utf-8 -*-
"""
    concert1.components
    ~~~~~~~~~~~~~~~~~~~

    Common application components

    :copyright: (c) 2013 by Concert Talent
    :license: see LICENSE for more details
    
"""
from flask.ext.assets import Environment
from flask.ext.login import LoginManager, AnonymousUser
#from flask_mail import Mail
from flask.ext.principal import Principal
from flask.ext.sqlalchemy import SQLAlchemy
#from config import DevelopmentConfig, DebugConfig, ProductionConfig, TestingConfig

db = SQLAlchemy()

login_manager = LoginManager()

principals = Principal()

#mail = Mail()

#: Current Configuration
'''
CONFIG = {
    'development': DevelopmentConfig,
    'debug': DebugConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
'''

class Anonymous(AnonymousUser):
    name = u"Anonymous"

assets = Environment()
