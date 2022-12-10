import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
import db
bp = Blueprint('auth', __name__, url_prefix='/', template_folder='templates', static_folder='static')

@bp.route('/', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        id = request.form['username']
        password = request.form['password']
        login_character = request.form.get('login_character')
        # db = db.get_db()
        error = None
        # cursor = db.cursor()
        if id.strip() == '':
            error = 'Id is required.'
        elif password.strip() == '':
            error = 'Password is required.'
        if error is None:
            # if user == "consumer":
            #   cursor.execute("SELECT consumer_id FROM Consumer WHERE consumer_id = %s", (id))
            # elif user == "plant owner":
            #   cursor.execute("SELECT owner_id FROM Plant_owner WHERE owner_id = %s", (id))
            # user = cursor.fetchone()

            # if user is None:
            #     error = 'Incorrect id.'
            # elif not check_password_hash(user['password'], password):
            #     error = 'Incorrect password.'

            # if error is None:
            #     session.clear()
            #     session['user_id'] = user['user_name']
            #     if user['privilege'] == 'normal':
            #         return redirect(url_for('index'))
            #     else:
            #         return  redirect(url_for('admin.admin'))
            
            return redirect(url_for(login_character+'.index_'+login_character))
            
            # return render_template('login.html', error = error)
        return render_template('login.html', error=error)
    return render_template('login.html')


@bp.route('/register', methods = ('GET','POST'))
def register():
    if request.method == 'POST':
        id = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        # db = db.get_db()
        error = None
        # cursor = db.cursor()
        if not id:
            error = 'Id is required.'
        elif not password:
            error = 'Password is required.'
        elif not password2:
            error = 'Please repeat password.'
        elif password != password2:
            error = 'Password is inconsistent.'
        # else:
            # if user == "consumer":
            #   cursor.execute("SELECT consumer_id FROM Consumer WHERE consumer_id = %s", (id))
            # elif user == "plant owner":
            #   cursor.execute("SELECT owner_id FROM Plant_owner WHERE owner_id = %s", (id))
            # if cursor.fetchone() is not None:
            #     error = 'User {} is already registered.'.format(id)

        if error is None:
            # if user == "consumer":
            #    cursor.execute("INSERT INTO Consumer(consumer_id, password) VALUES (%s, %s, %s)", (id, generate_password_hash(password)))
            # elif user == "plant owner":
            #    cursor.execute("INSERT INTO Plant_owner(owner_id, password) VALUES (%s, %s, %s)", (id, generate_password_hash(password)))
            # db.commit()
            return redirect(url_for('auth.login'))

        print('register page error is: ', error)
        # flash(error)
        return render_template('register.html', error = error)
    return render_template('register.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    g.user = user_id
    # if user_id is None:
    #     g.user = None
    # else:
    #     db = get_db()
    #     cursor = db.cursor()
    #     cursor.execute("SELECT * FROM User WHERE user_name = %s", (user_id))
    #     g.user = cursor.fetchone()

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
