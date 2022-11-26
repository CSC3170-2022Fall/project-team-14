# Work Distribution

| Student ID | Student Name | Work                      |
| ---------- | ------------ | ------------------------- |
| 118010246  | 秦兰          | Web page(Frond end)       |       
| 119010445  | 张新宇        | Web page(Frond end)       |
| 120090322  | 陈琳          | Document edit             |
| 120090171  | 张梦瑶        | ER Diagram and schema     |
| 120090702  | 李亿芊        | Database(back end)        |
|            |              | Database(back end)        |



# Project Structure
## Major Functionalities
- Register the package information that is released by some consumer
- Allow the consumer to appoint some plant for some package manually
- The assignment and the start-time of some operation with some machine could be further set under the constraint of plant appointment
- Once some operation is successfully finished, the processing record in end-time and expense could be written back.
- The production information, like manufacture capacity of some plant, or the demand changes of some consumer within some period of time can be calculated.
<br></br>

## Assumption

1. One consumer can have multiple packages.
2. One package refers to one type of chip. 
3. One plant holds one to many machines of the same type.
4. One machine can process one operation at the same time.
5. One operation in a package can be assigned to only one plant.
6. Processing record involves the start time, end time and expense of one operation processed on one machine.
7. If consumer doesn't appoint plant, our system will allocate one plant for him.
8. All processes(operations) of one package will be finished in the same plant, which means that the machine type of this plant will change after all chips finishes some process(operation).
9. If all the plants are busy, packages will be put in the waiting list. As soon as there is a free plant, package will be appoint.
<br></br>

## Schema Design: Chip Manufacture (__need to polish!!!__)

Reference(__see wechat group picture__)



### Entity

__consumer__(<u>consumer_ID</u>, password, package_ID)

__plant__(<u>plant_ID</u>, passward, machine_ID)

__package__(<u>package_ID</u>, consumer_ID, plant_ID, chip_Type, chip_Num)

__machine_type__(<u>machine_Type</u>, <u>operation_Type</u>, feasibility, time, expense, quota)

__machine__(<u>machine_ID</u>, machine_Type, plant_ID, status)

__chip_type__(number, precedency, operation_Type)

__chip__(<u>chip_Type</u>, plant_ID, machine_Type)

__operation_type__(feasibility, time, expense)

__operation__(<u>operation_Type</u>)

__handle_record__(<u>package_ID</u>, start_Time, end_Time, expense)

__proc_record__(<u>package_ID</u>, <u>operation_Type</u>, <u>machine_ID</u>, start_time, end_time, expense)
<br></br>



### Relationship

__chip_require_operation__(<u>chip_Type</u>, <u>operation_Type</u>, precedency)

__consumer_appoint_plant__(<u>consumer_ID</u>, <u>package_ID</u>, plant_ID )

__plant_assign_op_to_machine__(<u>plant_ID</u>,operation_Type, machine_ID, start_Time)

<br></br>

## Schema Design: Bank System

### Entity

__Account__(account_ID, passward, balance)

### Relationship

__Transfers__(transfer_ID, from_account_ID, to_account_ID, amount)



<br></br>

## ER Diagram
![image](https://user-images.githubusercontent.com/83419532/204088784-8308afd6-6382-4187-8fed-b271aca43bab.png)

<br></br>

# Implementation

## User Interface (frond end)

### Consumer
1. login page
- account
- password
2. home page
- Register package information ( link to payment page)
- My package
    - price
    - process
    - overall time
3. payment
- pop-up window
    - QR code( if user scans and pays, send a encryted arguments to the bank. Via redirection, the webpage can be directed to some "success/failure payment page" after the bank has processed the request)
    

### Plant owner (or worker)
1. login page
- account
- password
2. home page
- Package list( finished and waiting list all shown)
    - machine ID
        - operation type (can be changed by plant owner)
        - start-time (plant owner can set the start-time, or the actual start-time will be shown)
        - estimated end-time
        - actual end-time
        - expense
    


## Database (back end)


