# -*- coding: utf-8 -*-
"""
    concert1.security
    ~~~~~~~~~~~~~~~~~

    Flask-Security blueprint

    :copyright: (c) 2013 by Concert Talent
    :license: LICENSE, see LICENSE for more details.
    
"""

from flask import Blueprint
from concert1.security.views import (login, profile, post_login, post_logout,
    register)

security = Blueprint('security', __name__, url_prefix='/auth')

security.add_url_rule('/login', 'login', view_func=login)
security.add_url_rule('/profile', 'profile', view_func=profile)
security.add_url_rule('/post_login', 'post_login', view_func=post_login)
security.add_url_rule('/post_logout', 'post_logout', view_func=post_logout)
security.add_url_rule('/register', 'register', view_func=register, methods=("GET", "POST"))

'''
@security.route('/admin')
@roles_required('admin')
def admin():
    return render_template('security/index.html', content='Admin Page')

@security.route('/admin_or_editor')
@roles_accepted('admin', 'editor')
def admin_or_editor():
    return render_template('security/index.html', content='Admin or Editor Page')

@security.route('/activate/<activationid>')
def activate(activationid):
    key = get_or_abort(RegistrationKey, decode_id(activationid))
    user = user_datastore.with_id(key.user_id)
    active_user = user_datastore.activate_user(user.email)
    db.session.delete(key)
    db.session.commit()
    flash("Your account has been activated")
    return redirect(url_for('security.login'))
'''
