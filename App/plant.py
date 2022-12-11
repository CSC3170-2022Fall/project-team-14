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
    if(g.user):
        db = get_db()
        error = None
        cursor = db.cursor()
        package_list=[]
        temp =[]
        cursor.execute("SELECT package_id, chip_type, chip_number, consumer_id FROM Packages WHERE plant_id = %s",g.user)
        package_list_1 = cursor.fetchall()
        print(package_list_1[0][0])
        cursor.execute("SELECT start_time, status FROM Process_record WHERE package_id = %s", str(package_list_1[0][0]))
        package_list_2 = cursor.fetchall()
        print(package_list_1[0])
        print(package_list_2)
        # for i in range(0,4):
        #     package_list.append(package_list_1[0][i])
        # for j in range(0,2):
        #     package_list.append(package_list_2[0][j])
        package_list_11=package_list_1[0]+package_list_2[0]
        package_list.append(package_list_11)
        print(package_list)
        cursor.execute("SELECT machine_id, status, start_time, end_time FROM Process_record WHERE plant_id = 333")
        machine_list = cursor.fetchall()
        print(machine_list)
        return render_template('index_plant.html', package_list=package_list, machine_list=machine_list)


# @bp.route('/index_plant', methods=('GET', 'POST'))
# def packagelist():
#     # if (g.user):
#     #     if request.method == 'POST':
#             #plant_id = request.form["plant_id"]
#             db = get_db()
#             error = None
#             cursor = db.cursor()
#             cursor.execute("SELECT package_id, chip_type, chip_number, consumer_id FROM Packages WHERE plant_id = 333")
#             package_list_1 = cursor.fetchall()
#             cursor.execute("SELECT start_time, status FROM Process_record WHERE package_id = SELECT package_id FROM Packages WHERE plant_id = 333")
#             package_list_2 = cursor.fetchall()
#             package_list=package_list_1+package_list_2
#             cursor.execute("SELECT machine_id, status, start_time, end_time FROM Process_record WHERE plant_id = 333")
#             machine_list = cursor.fetchall()
#             print(machine_list)
            



#             return render_template('/index_plant.html', package_list=package_list, machine_list=machine_list)



@bp.route('/change_start_operation', methods=('GET', 'POST'))
def change_start_operation():
    if (g.user):
        if request.method == 'POST':
            db = get_db()
            cursor = db.cursor()
            machine_id=request.form['machine_id']
            start_time = request.form["start_time"]
            operation_type=request.form["operation_type"]
            cursor.execute("SELECT operation_type FROM Operation_machine_cost WHERE machine_id = %s", machine_id)
            operation_list = cursor.fetchall()
            if operation_type in operation_list:
                cursor.execute(
                                "UPDATE Process_record SET operation_type=%s, start_time = %s WHERE machine_id = %s", (operation_type,start_time, machine_id)
                                )    
                db.commit()  
            else:
                return redirect(url_for('plant.index_plant'))
                # error="This operation_type is unavaliable, please choose again!"
                # return render_template('/index_plant.html', error = error)
                
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


