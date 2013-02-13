# -*- coding: utf-8 -*-

import os, sys
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/google4fda8ef7d8ce7a73.html')
def google_webmaster_tools():
    return render_template('google4fda8ef7d8ce7a73.html')
