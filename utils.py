# utils.py
from functools import wraps
from flask import session, redirect, url_for, flash, request

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            # Save the URL the user was trying to access
            session['next_url'] = request.url
            flash("You need to enter the password first 🚫")
            return redirect(url_for('main.enter_password'))
        return f(*args, **kwargs)
    return decorated_function
