# -*- coding: utf-8 -*-
"""
    concert1.base
    ~~~~~~~~~~~~~

    base blueprint

    :copyright: (c) 2013 by Concert Talent
    :license: LICENSE, see LICENSE for more details.
    
"""

from flask import Blueprint
from concert1.base.views import index

base = Blueprint('base', __name__)

base.add_url_rule('/', 'index', view_func=index)
