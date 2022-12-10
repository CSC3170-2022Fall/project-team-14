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

@bp.route('/', methods=('GET', 'POST'))
def packagelist():
    if (g.user):
        if request.method == 'POST':
            plant_id = request.form["plant_id"]
            db = get_db()
            error = None
            cursor = db.cursor()
            cursor.execute("SELECT package_id, chip_type, chip_number, customer_id, start_time, status FROM Packages WHERE plant_id = %s", plant_id)
            package_list = cursor.fetchall()
        
            return render_template('/index_plant.html',package_list=package_list)

def machinelist():
    if (g.user):
        if request.method == 'POST':
            machine_id = request.form["machine_id"]
            db = get_db()
            error = None
            cursor = db.cursor()
            cursor.execute("SELECT machine_id, status, start_time, end_time FROM Process_record WHERE machine_id = %s", (machine_id))
            machine_list = cursor.fetchone()
            return render_template('/index_plant.html',machine_list=machine_list)

def change_start_time(): 
    if(g.user):
        db = get_db()
        cursor = db.cursor()
        machine_id=request.form["machine_id"]
        cursor.execute("SELECT operation_type FROM Machine WHERE machine_id =%s", (machine_id))
        operation_list = cursor.fetchall() 
        start_time = request.form["start_time"]
        operation_type=request.form["operation_type"]
        cursor.execute(
                        "INSERT INTO Process_record(machine_id, start_time, operation_type) VALUES (%s, %d, %s)",(machine_id, start_time, operation_type)
                        )
        
        new_time = cursor.fetchall() 
        db.commit()  
        return render_template('/index_plant.html',new_time=new_time)
