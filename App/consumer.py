from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort
from auth import login_required
from alg import generate_packageid, allocate_package_call
from db import get_db

bp = Blueprint('consumer', __name__)

@bp.route('/index_consumer')
def index_consumer():
    if(g.user):
        return render_template('index_consumer.html')
    return redirect(url_for('auth.login'))
    # return render_template('index_consumer.html')


@bp.route('/', methods=('GET', 'POST'))
def packagelist():
    if (g.user):
        if request.method == 'POST':
            package_id = request.form["package_id"]
            db = get_db()
            error = None
            cursor = db.cursor()
            cursor.execute("SELECT package_id, chip_type, chip_number, total_expense FROM Packages WHERE package_id = %s", (package_id))
            if cursor.fetchone() is not None:
                error = 'Package {} does not exist.'.format(package_id)
                return render_template('/consumer/packagelist.html', error = error)
            else:
                info1 = cursor.fetchone()
                cursor.execute("SELECT package_id, start_time, status FROM Process_record WHERE package_id = %s", package_id)
                info2 = cursor.fetchone()
                return render_template('consumer/packagelist.html', info1 = info1, info2 = info2)

@bp.route('/registerpackage', methods=('GET', 'POST'))
@login_required
def registerpackage():
    if (g.user):
        if request.method == 'POST':           
            package_id = generate_packageid()
            chip_type =  request.form['chip_type']
            chip_number = request.form['chip_number']
            plant_id = request.form['plant_id']

            error = None
            if not chip_type:
                error = "Chip type is required."
            elif not chip_number:
                error = "Chip number is required."
            elif not plant_id:
                db = get_db()
                cursor = db.cursor()
                plant_id = cursor.execute("SELECT plant_id From Machine WHERE status = %s", "finished").fetchone()
            
            if error is not None:
                flash(error)
            else:
                cursor.execute(
                    "SELECT expense From Chip_requires_operation WHERE chip_type = %s", chip_type
                    )
                total_expense = cursor.fetchone()*chip_number
                price = allocate_package_call(package_id, chip_type, chip_number, plant_id) 
                cursor.execute(
                    "INSERT INTO Package(package_id, chip_number, chip_type, plant_id, consumer_id, total_expense, price) VALUES (%s, %d, %s, %s, %s)",(package_id,chip_number,chip_type, plant_id,g.user[id],total_expense, price)
                    ) 
                db.commit()  
                return redirect(url_for('/payment'))
                  
        return render_template('consumer/registerpackage.html')
   
@bp.route('/payment')
@login_required
def payment():
    if (g.user):
        status = "fail"
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT total_expense FROM Package WHERE package_id = %s", g.user['package_id'])
        e = cursor.fetchone()
        # for bank schema
        error = None
        cursor.execute("SELECT balance FROM Consumer WHERE consumer_id = %s", g.user["consumer_id"])
        balance = cursor.fetchone()
        cursor.execute("SELECT price FROM Package WHERE package_id = %s", g.user["package_id"])
        price = cursor.fetchone()
        if balance - price > 0:
            cursor.execute("UPDATE FROM Consumer SET balance = %f WHERE consumer_id = %s", (balance-price, g.user["consumer_id"]))
            db.commit()
            status = 'success'
        else: 
            status = "fail"
        if status == 'success':
            return render_template('consumer/payment.html')
        else:
            return redirect(url_for("/consumer"))
        