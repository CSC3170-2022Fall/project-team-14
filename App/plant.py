from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash

from auth import login_required
from db import get_db


bp = Blueprint('plant', __name__)

@bp.route('/index_plant')
def index_plant():
    return render_template('index_plant.html')


@bp.route('/index_plant', methods=('GET', 'POST'))
def packagelist():
    if (g.user):
        if request.method == 'POST':
            plant_id = request.form["plant_id"]
            db = get_db()
            error = None
            cursor = db.cursor()
            cursor.execute("SELECT package_id, chip_type, chip_number, customer_id, start_time, status FROM Packages WHERE plant_id = %s", plant_id)
            package_list = cursor.fetchall()


            machine_id = request.form["machine_id"]
            db = get_db()
            error = None
            cursor = db.cursor()
            cursor.execute("SELECT machine_id, status, start_time, end_time FROM Process_record WHERE machine_id = %s", (machine_id))
            machine_list = cursor.fetchone()
            



            return render_template('/index_plant.html', package_list=package_list, machine_list=machine_list)



@bp.route('/change_start_operation', methods=('GET', 'POST'))
def change_start_operation():
    if (g.user):
        if request.method == 'POST':
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                            "INSERT INTO Process_record(package_id,operation_type,machine_id,start_time,end_time,plant_id,status) VALUES (%s,%s,%s,%s,%s,%s,%s)",(2,"2",2,2,2,3,"2")
                            ) 
            machine_id=request.form['machine_id']
            start_time = request.form["start_time"]
            operation_type=request.form["operation_type"]
            print(machine_id,start_time,operation_type)
            cursor.execute(
                            "UPDATE Process_record SET start_time = %s WHERE machine_id = %s", (start_time, machine_id)
                            )    
            db.commit()  
            # plant_id = request.form["plant_id"]
            # db = get_db()
            # error = None
            # cursor = db.cursor()
            # cursor.execute("SELECT package_id, chip_type, chip_number, customer_id, start_time, status FROM Packages WHERE plant_id = %s", plant_id)
            # package_list = cursor.fetchall()


            # machine_id = request.form["machine_id"]
            # db = get_db()
            # error = None
            # cursor = db.cursor()
            # cursor.execute("SELECT machine_id, status, start_time, end_time FROM Process_record WHERE machine_id = %s", (machine_id))
            # machine_list = cursor.fetchone()
            # return render_template('/index_plant.html', package_list=package_list, machine_list=machine_list)
        return redirect(url_for('plant.index_plant'))


