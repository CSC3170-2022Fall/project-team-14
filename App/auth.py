import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
import db
bp = Blueprint('auth', __name__, url_prefix='/', template_folder='templates', static_folder='static')

@bp.route('/login')
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = db.get_db()
        error = None
        cursor = db.cursor()
        if username.strip() == '':
            error = 'Username is required.'
        elif password.strip() == '':
            error = 'Password is required.'
        if error is None:
            cursor.execute("SELECT * FROM User WHERE user_name = %s", (username))
            user = cursor.fetchone()

            if user is None:
                error = 'Incorrect username.'
            elif not check_password_hash(user['password'], password):
                error = 'Incorrect password.'

            if error is None:
                session.clear()
                session['user_id'] = user['user_name']
                if user['privilege'] == 'normal':
                    return redirect(url_for('index'))
                else:
                    return  redirect(url_for('admin.admin'))

            return render_template('login.html', error = error)
        return render_template('login.html', error=error)
    return render_template('login.html')


@bp.route('/register', methods = ('GET','POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        # email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']
        # db = db.get_db()
        error = None
        # cursor = db.cursor()
        if not username:
            error = 'Username is required.'
        # elif not email:
        #     error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        elif not password2:
            error = 'Please repeat password.'
        elif password != password2:
            error = 'Password is inconsistent.'
        # else:
        #     # TODO: change the sql
        #     cursor.execute("SELECT user_name FROM User WHERE user_name = %s", (username))
        #     if cursor.fetchone() is not None:
        #         error = 'User {} is already registered.'.format(username)

        if error is None:
            # TODO: change the sql
            # cursor.execute("INSERT INTO User(user_name, password, email) VALUES (%s, %s, %s)", (username, generate_password_hash(password), email))
            # db.commit()
            return redirect(url_for('auth.login'))

        print('register page error is: ', error)
        # flash(error)
        return render_template('register.html', error = error)
    return render_template('register.html')

@bp.route('/login')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
