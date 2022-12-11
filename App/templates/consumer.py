from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort
from auth import login_required
from rand import generate_packageid
from db import get_db

bp = Blueprint('consumer', __name__)

@bp.route('/index_consumer')
def index_consumer():
    if(g.user):
        db = get_db()
        cursor = db.cursor()
        chip_type = []
        chips = cursor.execute("SELECT DISTINCT chip_type FROM Chip_expense")
        for i in range(chips):
            ttt = cursor.fetchone()
            chip_type.append(ttt)
        plant_id = []
        plants = cursor.execute("SELECT DISTINCT plant_id FROM Machine WHERE status = %s ORDER BY plant_id ASC", "IDLE")
        for i in range(plants):
            ttt = cursor.fetchone()
            plant_id.append(ttt)
        # display package list
        cursor.execute("SELECT package_id, chip_type, chip_number, plant_id, price FROM Packages WHERE consumer_id = %s", g.user)
        package_list = cursor.fetchall()
        return render_template('index_consumer.html',  package_list = package_list, chip_type = chip_type, plant_id = plant_id)
    # return redirect(url_for('auth.login'))
    return render_template('index_consumer.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


@bp.route('/searchpackage', methods=('GET', 'POST'))
def searchpackage():
    if (g.user):
        package_list = []
        packages = cursor.execute("SELECT package_id FROM Packages WHERE consumer_id = %s", g.user)
        for i in range(packages):
            ttt = cursor.fetchone()
            package_list.append(ttt)
        if request.method == 'POST':           
            package_id = request.form.get('package_id')
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT package_id, start_time, status FROM Process_record WHERE package_id = %s", package_id)
            package_id_list = cursor.fetchall()
        return render_template('index_consumer.html', package_list = package_list, package_id_list = package_id_list)

@bp.route('/registerpackage', methods=('GET', 'POST'))
@login_required
def registerpackage():
    if (g.user):
        # get all chip types and available plants
        if request.method == 'POST':           
            package_id = generate_packageid()
            db = get_db()
            cursor = db.cursor()
            chip_type =  request.form.get('chip_type')
            chip_number = request.form.get('chip_number')
            plant_id = request.form.get('plant_id')

            error = None
            if not chip_type:
                error = "Chip type is required."
            elif not chip_number:
                error = "Chip number is required."
            elif not plant_id:
                cursor.execute("SELECT plant_id From Machine WHERE status = %s", "finished")
                plt =  cursor.fetchone()
                plant_id = plt[0]
            if error is not None:
                flash(error)
            else:
                cursor.execute("SELECT price From Chip_expense WHERE chip_type = %s", chip_type)
                price = cursor.fetchone()
                cursor.execute(
                    "INSERT INTO Packages(package_id, chip_number, chip_type, plant_id, consumer_id, total_expense, price) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (package_id,chip_number,chip_type, plant_id, g.user, price[0]*int(chip_number), 1.2*price[0]*int(chip_number))) 
                db.commit()  
                return redirect(url_for('consumer.payment', package_id = package_id))
        return render_template('index_consumer.html', error = error)

@bp.route('/payment/<package_id>')
@login_required
def payment(package_id):
    if (g.user):
        db = get_db()
        cursor = db.cursor()
        error = None
        success = False
        cursor.execute("SELECT balance FROM Consumer WHERE consumer_id = %s", g.user)
        balance = cursor.fetchone()
        cursor.execute("SELECT chip_number, chip_type, plant_id, price FROM Packages WHERE package_id = %s", package_id)
        package = cursor.fetchall()
        cursor.execute("SELECT price FROM Packages WHERE package_id = %s", package)
        price = cursor.fetchone()
        if balance[0] - price[0] > 0:
            cursor.execute("UPDATE Consumer SET balance = %s WHERE consumer_id = %s", (balance[0]-price[0], g.user))
            db.commit()
            print("Payment is successful. Your package id is:",package)
            success = False
            return redirect(url_for('consumer.index_consumer'))
        else: 
            error = "Your balance is not available, payment fails."
        print("Your payment error is:", error)
        flash(error)
        return render_template('payment.html', balance = balance, package = package, success = success, error = error)
    return render_template('payment.html', balance = balance, package = package, success = success, error = error)

        