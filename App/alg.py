import queue
import time
import queue
import random
from db import get_db
#[[time,op,pack_id or mac_id, pred or opr_type or pred)]]
#op=1:allcoate:pack_id,pred
#op=2:change_start_time:mac_id,opr_type
#op=3:package stage end:pack_id,pred
#op=4:machine end: mac_id, plack_id, opr_type

global global_start_time
global_start_time = time.time()
global time_queue
time_queue = queue.PriorityQueue()

def search_call():
    cur_time = int((time.time() - global_start_time)*100)
    print("enter search_call with ",cur_time)    
    while (time_queue.empty() == False):
        next_exe = time_queue.get()
        print("next execution is ",next_exe)
        if(next_exe[0] > cur_time):
            time_queue.put(next_exe)
            break
        handle(next_exe)
        if(time_queue.empty()):
            break

def change_start_call(machine_id, start_time, operation_type):
    cur_time = int((time.time() - global_start_time)*100)
    time_queue.put([cur_time+start_time,3,machine_id,operation_type])

def allocate_package_call(package_id, chip_type, chip_number, plant_id=-1):
    db = get_db()
    cursor = db.cursor()
    cur_time = int((time.time() - global_start_time)*100)
    print("enter a new package with plant id %s",plant_id)

    if(plant_id != -1 or plant_id != None):
        #modify package
        print("allocate one package to plant %s",plant_id)
        cursor.execute("UPDATE Packages SET Packages.plant_id  = %s WHERE Packages.package_id  = %s",(plant_id,package_id))
        time_queue.put([cur_time,4,package_id,0])
        
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
                            if (machine[m]['status'] == 'IDLE'and (machine[m]['operation_type'] == None or machine[m]['operation_type'] == first_operation_type)):
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
            print("allocate one package to plant %s",now_plant_id)
            cursor.execute("UPDATE Packages SET Packages.plant_id  = %s WHERE Packages.package_id  = %s",(now_plant_id,package_id))
            time_queue.put([cur_time,4,package_id,0])
            
        elif can_plant_id != -1:
            #modify package
            cursor.execute("UPDATE Packages SET Packages.plant_id  = %s WHERE Packages.package_id  = %s",(can_plant_id,package_id))
            time_queue.put([cur_time,4,package_id,0])

        else:
            print("Error! cannot allocate that package!")





def handle(next_exe):
    db = get_db()
    cursor = db.cursor()
    if(next_exe[1] == 4): #package exe next operation
        exe_time,op,package_id,pred  = next_exe
        #select *  from package where package_id
        cursor.execute("SELECT * from Packages where Packages.package_id = %s",package_id)
        package_info = cursor.fetchall()
        print("package_info",package_info)
        # select next_opr from c_r_o where chip_type and pred
        cursor.execute("SELECT operation_type FROM Chip_requires_operation WHERE (Chip_requires_operation.chip_type = %s and Chip_requires_operation.precedency  = %s)",(package_info[0][2],pred))
        next_operation_type_tuple = cursor.fetchall()
        print("next_operation_type_tuple",next_operation_type_tuple)
        next_operation_type = next_operation_type_tuple[0][0]

        # select mac_id, quota from machine where plant_id, opr_type, status
        cursor.execute("SELECT * FROM Machine WHERE (Machine.plant_id = %s and Machine.status = %s and (Machine.operation_type is Null or Machine.operation_type = %s))",
        (package_info[0][3],'IDLE',next_operation_type))
        machine_info = cursor.fetchall()
        print("machine_info",machine_info)
        sum = 0
        for cd in range(len(machine_info)):# sum quota up to see if enough
            sum += int(machine_info[cd][4])
        
        if sum >= package_info[0][1]:
            total_expense  = package_info[0][5]
            remain_number = package_info[0][1]
            actual_end_time = 0
            estimated_end_time = 0

            for i in range(len(machine_info)):
                cursor.execute("SELECT * FROM Operation_machine_cost WHERE (Operation_machine_cost.machine_id = %s and Operation_machine_cost.operation_type = %s)",
                (machine_info[i][0],next_operation_type))
                mac_opr = cursor.fetchall()
                print("mac_opr",mac_opr)
                print("total_expense before",total_expense)
                total_expense  = total_expense + mac_opr[0][3]*min(machine_info[i][4],remain_number)
                print("total_expense after",total_expense)
                cursor.execute("UPDATE Packages SET total_expense = %s WHERE  Packages.package_id = %s",
                (total_expense,package_id))
                cursor.execute("SELECT * from Packages where Packages.package_id = %s",package_id)
                package_info = cursor.fetchall()
                print("package_info after update total_expense",package_info)
                estimated_end_time_machine = next_exe[0] + mac_opr[0][2]*min(machine_info[i][4],remain_number)
                estimated_end_time = max(estimated_end_time,estimated_end_time_machine)
                actual_end_time_machine = estimated_end_time_machine + random.randint(-5,5)
                actual_end_time = max(actual_end_time_machine,actual_end_time)
                # modify status from machine
                cursor.execute("UPDATE Machine set Machine.status  = 'RUNNING' WHERE Machine.machine_id = %s",machine_info[i][0])
                remain_number -= int(machine_info[i][4])
                # modify status, expense, start_time, end_time in proc_record for a machine in proc_record!!!
                cursor.execute("INSERT `Process_record`(`package_id`,`operation_type`,`machine_id` ,`start_time`,`end_time` ,`plant_id` ,`status` ) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (package_id,next_operation_type,machine_info[i][0],next_exe[0],estimated_end_time,package_info[0][3],"RUNNING"))#mac_opr[0][3],
                time_queue.put([actual_end_time_machine,1,machine_info[i][0],package_id,next_operation_type])
                print("begin to execute in  one machine")
                if remain_number <= 0:
                    print("finish allocate!") 
                    break
            time_queue.put([actual_end_time,2,package_id,pred])

        else:# not enough, busy waiting 
            next_exe[0] += 1
            time_queue.put(next_exe)


    if(next_exe[1] == 3): #change operation 
        #modify machine
        #check if IDLE
        cursor.execute("SELECT * FROM Machine WHERE Machine.machine_id = %s",next_exe[2])
        machine_status = cursor.fetchall()
        if(machine_status[0][3] == 'IDLE'):
            print("suc change start time for %s, %s",(next_exe[3],next_exe[2]))
            cursor.execute("UPDATE Machine SET Machine.operation_type = %s WHERE Machine.machine_id = %s",(next_exe[3],next_exe[2]))
        else:
            #print("CANNOT change start time as expected!")
            next_exe[0] = -1
            time_queue.put(next_exe)


    if(next_exe[1] == 2):#package end one step
        cursor.execute("SELECT * FROM Packages WHERE Packages.package_id = %s",next_exe[2])
        Packages_info = cursor.fetchall()
        cursor.execute("SELECT * FROM Chip_requires_operation WHERE Chip_requires_operation.chip_type  = %s",Packages_info[0][2])
        chip_info = cursor.fetchall()
        pred_num = len(chip_info)

        if pred_num < next_exe[3]:
            print("ERROR! OUT OF STAGE")
        elif (pred_num-1) == next_exe[3]:#reach end
            #get total_expense and price
            cursor.execute("SELECT * FROM Packages WHERE Packages.package_id = %s",next_exe[2])
            Packages_info = cursor.fetchall()
            package_income = Packages_info[0][6] - Packages_info[0][5]
            print("the pacakge is end! with income:",package_income)
            #modify Own
            cursor.execute("UPDATE Own SET Own.income = Own.income+%s WHERE Own.plant_id = %s",(package_income,next_exe[2]))
        else:#need to allocate next step
            next_exe[3] += 1 #pred
            next_exe[1] = 4 #allocate type
            time_queue.put(next_exe)


    if(next_exe[1] == 1):#machine end
        print("one machine end named %d",next_exe[2])
        #modify machine's status and operation_type
        cursor.execute("UPDATE Machine SET Machine.status = 'IDLE' WHERE Machine.machine_id = %s",next_exe[2])
        cursor.execute("UPDATE Machine SET Machine.operation_type = NULL WHERE Machine.machine_id = %s",next_exe[2])
        #modify end time for process record
        cursor.execute("UPDATE Process_record set Process_record.end_time = %s WHERE (Process_record.package_id = %s and Process_record.operation_type = %s and Process_record.machine_id = %s)",(next_exe[0], next_exe[3],next_exe[4],next_exe[2]))
