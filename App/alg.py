from asyncio.windows_events import NULL
import queue
import time
import queue
import random
from db import get_db
#[[time,op,pack_id or mac_id, pred or opr_type or pred)]]
#op=1:allocate, pack_id,pred
#op=2:change_start_time, mac_id,opr_type
#op=3:package stage end, pack_id,pred
#op=4:machine end, mac_id

global_start_time = int(time.time())
time_queue = queue.PriorityQueue()

def change_start_call(machine_id, start_time, operation_type):
    time_queue.put([int(time.time())-global_start_time+start_time,2,machine_id,operation_type])

def allocate_package_call(package_id, chip_type, chip_number, plant_id=-1):
    db = get_db()
    cursor = db.cursor()
    cur_time = int(time.time()) - global_start_time

    if(plant_id != -1):
        #modify package
        cursor.execute("UPDATE Packages SET Packages.plant_id  = %d WHERE Packages.package_id  = %d",plant_id,package_id)
        time_queue.put(-1,1,package_id,0)
        
    else:
        #select opr_type,pred from c-r-o where chip_type
        cursor.execute("SELECT * FROM Chip_requires_operation WHERE Chip_requires_operation.chip_type = %s",chip_type)
        operation_type = cursor.fetchall()
        #select plant_id from own
        cursor.execute("SELECT DISTINCT plant_id FROM Own")
        all_plant_id = cursor.fetchall()

        now_plant_id = -1
        can_plant_id = -1
        for p in range(len(all_plant_id)):
            #select* from machine where plant_id equal
            cursor.execute("SELECT * FROM Machine WHERE Machine.plant_id = %s",all_plant_id[p]['plant_id'])
            machine = cursor.fetchall() #machine is all mac in plant p
            now = True 
            can = True
            for o in range(len(operation_type)):
                count_can = 0
                count_now = 0

                if operation_type[o]['precedency'] == 0:
                    first_operation_type = operation_type[o]['operation_type']

                for m in range(len(machine)):
                    #select operation_type from Operation_machine_cost where machine_id
                    cursor.execute("SELECT operation_type FROM Operation_machine_cost WHERE Operation_machine_cost.machine_id = %s",machine[m]['machine_id'])
                    one_machine_can_opr = cursor.fetchall()
                    for one_can in range(len(one_machine_can_opr)):
                        if(one_machine_can_opr[one_can]['operation_type'] == operation_type[o]['operation_type']):
                            count_can += int(machine[m]['quota'])
                            if (machine[m]['status'] == 'Idle'and (machine[m]['operation_type'] == NULL or machine[m]['operation_type'] == first_operation_type)):
                                count_now += int(machine[m]['quota'])

                    if count_now >= chip_number:#one operation can now
                        break

                if count_now >= chip_number:#this opr can done now, change to next opr
                    continue

                if (now == True) and (count_now < chip_number):#one opr that cannot now exe
                    now = False

                if count_can < chip_number:#one opr cannot done by plant p, no need to check other opr
                    can = False
                    break
                

            if now == True: #after checking all opr
                now_plant_id = all_plant_id[p]['plant_id']
                break
            if (can == True) and (can_plant_id == -1): 
                can_plant_id = all_plant_id[p]['plant_id']


        if now_plant_id != -1:
            #modify plant_id in package
            cursor.execute("UPDATE Packages SET Packages.plant_id  = %d WHERE Packages.package_id  = %d",now_plant_id,package_id)
            time_queue.put([-1,1,package_id,0])
            
        elif can_plant_id != -1:
            #modify package
            cursor.execute("UPDATE Packages SET Packages.plant_id  = %d WHERE Packages.package_id  = %d",can_plant_id,package_id)
            time_queue.put([-1,1,package_id,0])

        else:
            print("Error! cannot allocate that package!")





def main():
    db = get_db()
    cursor = db.cursor()
    while(True):
        cur_time = int(time.time()) - global_start_time
        next_exe = time_queue.get()
        while(next_exe[0] <= cur_time):
            if(next_exe[1] == 1): #package exe next operation
                exe_time,op,package_id,pred  = next_exe
                #select plant_id, chip_number, total_expense  from package where package_id
                cursor.execute("SELECT * from Packages where Packages.package_id = %d",package_id)
                package_info = cursor.fetchall()
                # select next_opr from c_r_o where chip_type and pred
                cursor.execute("SELECT operation_type FROM Chip_requires_operation WHERE (Chip_requires_operation.chip_type = %s and Chip_requires_operation.precedency  = %d)",package_info[0]['chip_type'],pred)
                next_operation_type_tuple = cursor.fetchall()
                next_operation_type = next_operation_type_tuple[0]['operation_type']
                # select mac_id, quota from machine where plant_id, opr_type, status
                cursor.execute("SELECT * FROM Machine WHERE (Machine.plant_id = %d and Machine.status = %s and (Machine.operation_type = Null or Machine.operation_type = %s))",package_info[0]['plant_id'],'Idle',next_operation_type)
                machine_info = cursor.fetchall()
                sum = 0
                for cd in range(len(machine_info)):# sum quota up to see if enough
                    sum += int(machine_info[cd]['quota'])
                
                if sum >= package_info[0]['chip_number']:
                    total_expense  = package_info[0]['total_expense ']
                    remain_number = package_info[0]['chip_number']
                    actual_end_time = 0
                    estimated_end_time = 0

                    for i in range(len(machine_info)):
                        total_expense  = total_expense + machine_info[i]['expense']*min(machine_info[i]['quota'],remain_number)
                        estimated_end_time_machine = cur_time + min(machine_info[i]['time'],remain_number)
                        estimated_end_time = max(estimated_end_time,estimated_end_time_machine)
                        actual_end_time_machine = estimated_end_time_machine + random.randint(-50,50)
                        actual_end_time = max(actual_end_time_machine,actual_end_time)
                        # modify status from machine
                        cursor.execute("UPDATE Machine set Machine.status  = 'Running' WHERE Machine.machine_id = %s",machine_info[i]['machine_id'])
                        remain_number -= int(machine_info[i]['quota'])
                        if remain_number <= 0: 
                            break
                        # modify status, expense, start_time, end_time in proc_record for a machine
                        cursor.execute("UPDATE Process_record set Process_record.status = %s and Process_record.expense = %f and Process_record.start_time = %d and Process_record.end_time = %d WHERE (Process_record.package_id = %d and Process_record.operation_type = %s and Process_record.machine_id = %d)",'Running',machine_info[i]['expense'],cur_time,estimated_end_time, package_id,next_operation_type,machine_info[i]['machine_id'])
                        time_queue.put([actual_end_time_machine,4,machine_info[i]['machine_id']])
                    
                    time_queue.put([actual_end_time,3,package_id,pred])

                else:# not enough busy waiting 
                    time_queue.put(next_exe)


            if(next_exe[1] == 2): #change operation 
                #modify machine
                #check if Idle
                cursor.execute("SELECT * FROM Machine WHERE Machine.machine_id = %d",next_exe[2])
                machine_status = cursor.fetchall()
                if(machine_status[0]['status'] == 'Idle'):
                    cursor.execute("UPDATE Machine SET Machine.operation_type = %s WHERE Machine.machine_id = %d",next_exe[3],next_exe[2])
                else:
                    #print("CANNOT change start time as expected!")
                    next_exe[0] = 0
                    time_queue.put(next_exe)


            if(next_exe[1] == 3):#package end one step
                cursor.execute("SELECT * FROM Packages WHERE Packages.package_id = %d",next_exe[2])
                Packages_info = cursor.fetchall()
                cursor.execute("SELECT * FROM Chip_requires_operation WHERE Chip_requires_operation.chip_type  = %s",Packages_info[0]['chip_type'])
                chip_info = cursor.fetchall()
                pred_num = len(chip_info)

                if pred_num < next_exe[3]:
                    print("ERROR! OUT OF STAGE")
                elif pred_num == next_exe[3]:#reach end
                    #get total_expense and price
                    cursor.execute("SELECT * FROM Packages WHERE Packages.package_id = %d",next_exe[2])
                    Packages_info = cursor.fetchall()
                    package_income = Packages_info[0]['price'] - Packages_info[0]['total_expense']
                    #modify Own
                    cursor.execute("UPDATE Own SET Own.income = Own.income+%d WHERE Own.plant_id = %d",package_income,next_exe[2])
                else:#need to allocate next step
                    next_exe[3] += 1 #pred
                    next_exe[1] = 1 #allocate type
                    time_queue.put(next_exe)


            if(next_exe[1] == 4):#machine end
                #modify machine's status and operation_type
                cursor.execute("UPDATE Machine SET Machine.status = 'Idle' and Machine.operation_type = NULL WHERE Machine.machine_id = %d",next_exe[2])


            next_exe = time_queue.get()


        if next_exe[0] > cur_time:
            time_queue.put(next_exe)

        time.sleep(1)

