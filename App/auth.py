import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/', template_folder='templates', static_folder='static')

@bp.route('/')
def login():
    return render_template('login.html')


@bp.route('/')
def register():
    return render_template('register.html')

@bp.route('/')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))