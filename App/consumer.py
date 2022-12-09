from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash

from auth import login_required
from db import get_db
import db

bp = Blueprint('consumer', __name__)

@bp.route('/<string:id>/registerpackage', methods=('GET', 'POST'))
def registerpackage():
    if (g.user):
        if request.method == 'POST':
            # TO DO: generate random package id or ask user for id ?
            package_id = request.form["package_id"]
            chip_type =  request.form['chip_type']
            chip_number = request.form['chip_number']
            plant_id = request.form['plant_id']
            # redirect(url_for('consumer.payment'))
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO Package(package_id, chip_number, chip_type, plant_id, consumer_id) VALUES (%s, %d, %s, %s, %s)",(generate_password_hash(package_id),chip_number,chip_type, plant_id,g.user[id]))          
            db.commit()
    return render_template('consumer.registerpackage.html')

@bp.route('/<string:id>/checkpackage',methods=('GET','POST'))
def checkpackage():
    if (g.user):
        if request.method == 'POST':
            package_id = request.form["package_id"]
            db = db.get_db()
            error = None
            cursor = db.cursor()
            cursor.execute("SELECT package_id FROM Packages WHERE package_id = %s", (check_password_hash(g.user['package_id'],package_id)))
            if cursor.fetchone() is not None:
                error = 'Package {} does not exist.'.format(package_id)
                return render_template('consumer.checkpackage.html', error = error)
            else:
                return redirect(url_for('consumer.mypackage'))

@bp.route('/mypackage',methods=('GET', 'POST'))
def mypackage():
    if (g.user):
        cursor = db.cursor()
        cursor.execute("SELECT package_id, start_time, end_time, expense FROM Process_record WHERE package_id = %s", generate_password_hash(g.user['package_id']))
        info = cursor.fetchone()
        return render_template('mypackage.html', info=info)
    else:
        return redirect(url_for('auth.home'))
            
@bp.route('/payment', methods=('GET', 'POST'))
def payment():
    if (g.user):
        status = "fail"
        cursor = db.cursor()
        cursor.execute("SELECT expense FROM Process_record WHERE package_id = %s", generate_password_hash(g.user['package_id']))
        e = cursor.fetchone()
        # for bank schema
        # error = None
        # cursor.execute("SELECT balance FROM Account WHERE user_id = %s", balance)
        # b = cursor.fetchone()
        # if b - e > 0:
        #     cursor.execute("UPDATE FROM Account SET balance = %f WHERE user_id = %s", (balance, b-e))
        #     status = 'success'
        # else: 
        #     status = "fail"
        if status == 'success':
            # show in this page: expense = e, balance = b - e
            return redirect(url_for("consumer.registerpackage"))
        