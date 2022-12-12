from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort
from auth import login_required
from rand import generate_packageid
from db import get_db
import alg

bp = Blueprint('consumer', __name__)

@bp.route('/index_consumer')
def index_consumer():
    if(g.user):
        return render_template('index_consumer.html')
    return redirect(url_for('auth.login'))
    # return render_template('index_consumer.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


@bp.route('/')
def packagelist():
    if (g.user):
        if request.method == 'POST':
            package_id = request.form.get("package_id")
            db = get_db()
            error = None
            cursor = db.cursor()
            cursor.execute("SELECT package_id, chip_type, chip_number, price FROM Packages WHERE package_id = %s", (package_id))
            if cursor.fetchone() is not None:
                error = 'Package {} does not exist.'.format(package_id)
                return render_template('consumer/packagelist.html', error = error)
            else:
                list1 = cursor.fetchall()
                info1 = [i for i in range(len(list1))]
                cursor.execute("SELECT package_id, start_time, status FROM Process_record WHERE package_id = %s", package_id)
                list2 = cursor.fetchall()
                info2 = [i for i in range(len(list2))]
                return render_template('consumer/packagelist.html', info1 = info1, info2 = info2)

@bp.route('/registerpackage', methods=('GET', 'POST'))
@login_required
def registerpackage():
    if (g.user):
        if request.method == 'POST':           
            package_id = generate_packageid()
            db = get_db()
            cursor = db.cursor()

            chip_type_list = []
            chips = cursor.execute("SELECT * FROM Chip_expense").fetchall()
            for i in range(len(chips)):
                chip_type_list.append(i)
            plant_id_list = []
            plants = cursor.execute("SELECT * FROM OWn").fetchall()
            for i in range(len(plants)):
                plant_id_list.append(i)

            chip_type =  request.form.get('chip_type')
            chip_number = request.form.get('chip_number')
            plant_id = request.form.get('plant_id')

            error = None
            if not chip_type:
                error = "Chip type is required."
            elif not chip_number:
                error = "Chip number is required."
            elif not plant_id:
                plant_id = cursor.execute("SELECT plant_id From Machine WHERE status = %s", "finished").fetchone()
            
            if error is not None:
                flash(error)
            else:
                price = cursor.execute(
                    "SELECT price From Chip_expense WHERE chip_type = %s", chip_type
                    ).fetchone()
                cursor.execute(
                    "INSERT INTO Package(package_id, chip_number, chip_type, plant_id, consumer_id, price) VALUES (%s, %d, %s, %s, %s)",(package_id,chip_number,chip_type, plant_id,g.user['consumer_id'], price)
                    ) 
                db.commit()  
                alg.allocate_package_call(package_id,chip_type,int(chip_number),plant_id)
                return redirect(url_for('consumer.payment'))

   
@bp.route('/payment')
@login_required
def payment():
    if (g.user):
        db = get_db()
        cursor = db.cursor()
        error = None
        cursor.execute("SELECT balance FROM Consumer WHERE consumer_id = %s", g.user["consumer_id"])
        balance = cursor.fetchone()
        cursor.execute("SELECT price FROM Package WHERE package_id = %s", g.user["package_id"])
        price = cursor.fetchone()
        if balance - price > 0:
            cursor.execute("UPDATE FROM Consumer SET balance = %f WHERE consumer_id = %s", (balance-price, g.user["consumer_id"]))
            db.commit()
            print("Payment is successful. Your package id is:",g.user["package_id"])
            return redirect(url_for('consumer.index_consumer'))
        else: 
            error = "Your balance is not available, payment fails."
        print("Your payment error is:", error)
        flash(error)
        return render_template('payment.html', error = error)
    return render_template('payment.html')

# def return_button():
#     return redirect(url_for('index_consumer'))
        