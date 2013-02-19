#!/usr/bin/env python

import datetime

from flask import render_template

def index():
    return render_template(
                'index.html',
                #config=app.config,
                now=datetime.datetime.now,
            )
