import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

# from App.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))

def register():
    # if request.method == 'POST':
    #     username = request.form['username']
    #     email = request.form['email']
    #     password = request.form['password']
    #     password2 = request.form['password2']
    #     # db = get_db()
    #     error = None
    #     # cursor = db.cursor()
    #     if not username:
    #         error = 'Username is required.'
    #     # elif not email:
    #     #     error = 'Email is required.'
    #     elif not password:
    #         error = 'Password is required.'
    #     elif not password2:
    #         error = 'Please repeat password.'
    #     elif password != password2:
    #         error = 'Password is inconsistent.'
    #     # else:
    #         # TODO: 从数据库中检查是否已经有该用户
        
    #     # if error is None:
    #         # TODO: 将用户录入数据库
        
    #     print('register page error is: ', error)
    #     return render_template('register.html', error = error)
    return render_template('register.html')
