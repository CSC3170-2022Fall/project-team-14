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
        packages = cursor.execute("SELECT package_id FROM Packages WHERE consumer_id = %s", g.user)
        for i in range(packages):
            ttt = cursor.fetchone()
            package_list.append(ttt)
        if request.method == 'POST':           
            package_id = request.form.get('package_id')
            cursor.execute("SELECT package_id, start_time, status FROM Process_record WHERE package_id = %s", package_id)
            package_id_list = cursor.fetchall()
        return render_template('index_consumer.html', package_list = package_list, chip_type = chip_type, plant_id = plant_id, package_id_list = package_id_list)

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
                cursor.execute("SELECT balance FROM Consumer WHERE consumer_id = %s", g.user)
                balance = cursor.fetchone()
                package_info = []
                package_info.append(package_id)
                package_info.append(chip_number)
                package_info.append(chip_type)
                package_info.append(plant_id)
                package_info.append(1.2*price[0]*int(chip_number))   
                package_info.append(balance[0])   
                return render_template('payment.html', package = package_info)          
        return render_template('index_consumer.html', plant_id = plant_id, chip_type = chip_type, error = error)

@bp.route('/payment/<package>', methods=('GET', 'POST'))
@login_required
def payment(package):
    error = None
    if (g.user):
        db = get_db()
        cursor = db.cursor()  
        success = False   
        cursor.execute("SELECT balance FROM Consumer WHERE consumer_id = %s", g.user)
        balance = cursor.fetchone()
        package = package.replace('\'', '')
        package = package.replace('[', '')
        package = package.replace(']', '')
        info = package.split(',')
        price = float(info[4])
        if balance[0] - price >= 0:      
            cursor.execute(
                "INSERT INTO Packages(package_id, chip_number, chip_type, plant_id, consumer_id, total_expense, price) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (int(info[0]),int(info[1]),info[2], int(info[3]),g.user, info[4], price*1.2))  
            cursor.execute("UPDATE Consumer SET balance = %s WHERE consumer_id = %s", (balance[0]-price, g.user))
            db.commit()
            alg.allocate_package_call(int(info[0]),info[2],int(info[1]),int(info[3]))
            success = True
            print("Payment is successful. Your package id is:",package[0])
            if request.method == "POST":
                info[5] = balance[0]-price
                return render_template('payment.html', balance = balance[0]-price, package = info, success = success, error = error)
        else: 
            error = "Your balance is not available, payment fails."
            print("Your payment error is:", error)
            flash(error)
            return render_template('payment.html',  package = info, success = success, error = error)
    return render_template('payment.html',  package = info, success = success, error = error)

@bp.route('/payreturn', methods=('GET', 'POST'))
@login_required
def payreturn():

    return redirect(url_for('consumer.index_consumer'))
