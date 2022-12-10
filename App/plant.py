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
            package_id = request.form["package_id"]
            db = get_db()
            error = None
            cursor = db.cursor()
            cursor.execute("SELECT package_id, chip_type, chip_number, total_expense FROM Packages WHERE package_id = %s", (package_id))
            if cursor.fetchone() is not None:
                error = 'Package {} does not exist.'.format(package_id)
                return render_template('/plant/packagelist.html', error = error)
            else:
                info1 = cursor.fetchone()
                cursor.execute("SELECT package_id, start_time, status FROM Process_record WHERE package_id = %s", package_id)
                info2 = cursor.fetchone()
                return render_template('plant/packagelist.html', info1 = info1, info2 = info2)

def machinelist():
    if (g.user):
        if request.method == 'POST':
            machine_id = request.form["machine_id"]
            db = get_db()
            error = None
            cursor = db.cursor()
            cursor.execute("SELECT machine_id, status, start_time, end_time FROM Process_record WHERE machine_id = %s", (machine_id))
            info = cursor.fetchone()
            return redirect(url_for('/machinelist.html'),info=info)

def change_start_time(): 
    if(g.user):
        db = get_db()
        cursor = db.cursor()
        start_time = request.form["start_time"]
        cursor.execute(
                        "INSERT INTO Process_record(machine_id, start_time, operation_type) VALUES (%s, %d, %s)",(machine_id, start_time, operation_type)
                        ) 
        db.commit()  
        return redirect(url_for('/machinelist.html'))
