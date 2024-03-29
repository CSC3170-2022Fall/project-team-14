import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from db import get_db
bp = Blueprint('auth', __name__, url_prefix='/', template_folder='templates', static_folder='static')

@bp.route('/', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # consumer = request.form['login_consumer']
        # plant = request.form['login_plant']
        login_character = request.form.get('login_character')
        db = get_db()
        error = None
        cursor = db.cursor()
        if error is None:
            if login_character=="consumer":
              cursor.execute("SELECT consumer_id, password FROM Consumer WHERE consumer_id = %s", (username))
            elif login_character=="plant":
              cursor.execute("SELECT owner_id, password FROM Plant_owner WHERE owner_id = %s", (username))
            user = cursor.fetchone()

            if user is None:
                error = 'Incorrect id.'
            elif not check_password_hash(user[1], password):
                error = 'Incorrect password.'

            if error is None:
                session.clear()
                session['user_id'] = user[0]
                if login_character=="consumer":
                    return redirect(url_for('consumer.index_consumer'))
                elif login_character=="plant":
                    return redirect(url_for('plant.index_plant'))
            session['user_id'] = username
            # return redirect(url_for(login_character+'.index_'+login_character))
            
            return render_template('login.html', error = error)
        return render_template('login.html', error=error)
    return render_template('login.html')


@bp.route('/register_consumer', methods = ('GET','POST'))
def register_consumer():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        consumer = None
        db = get_db()
        error = None
        cursor = db.cursor()
        if password != password2:
            error = 'Password is inconsistent.'
        else:
            cursor.execute("SELECT consumer_id FROM Consumer WHERE consumer_id = %s", (username))
            if cursor.fetchone() is not None:
                error = 'User {} is already registered.'.format(username)

        if error is None:
            cursor.execute("INSERT INTO Consumer(consumer_id, password, balance) VALUES (%s, %s, %s)", (username, generate_password_hash(password),1000000))
            db.commit()
            return redirect(url_for('auth.login'))

        print('register page error is: ', error)
        flash(error)
        return render_template('register_consumer.html', error = error)
    return render_template('register_consumer.html')

@bp.route('/register_owner', methods = ('GET','POST'))
def register_owner():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        plant_id_list = request.values.getlist("plant_id")
        plant = None
        db = get_db()
        error = None
        cursor = db.cursor()
        if password != password2:
            error = 'Password is inconsistent.'
        else:
            cursor.execute("SELECT owner_id FROM Plant_owner WHERE owner_id = %s", (username))
            if cursor.fetchone() is not None:
                error = 'User {} is already registered.'.format(username)

        if error is None:
            cursor.execute("INSERT INTO Plant_owner(owner_id, password) VALUES (%s, %s)", (username, generate_password_hash(password)))
            for i in range(len(plant_id_list)):
                cursor.execute("UPDATE Own SET owner_id = %s WHERE plant_id = %s", (username, plant_id_list[i]))
            db.commit()
            return redirect(url_for('auth.login'))

        print('register page error is: ', error)
        flash(error)
        return render_template('register_owner.html', error = error)
    return render_template('register_owner.html')

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
