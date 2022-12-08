[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=9422486&assignment_repo_type=AssignmentRepo)
# CSC3170 Course Project

## Project Overall Description

This is our implementation for the course project of CSC3170, 2022 Fall, CUHK(SZ). For details of the project, you can refer to [project-description.md](project-description.md). In this project, we will utilize what we learned in the lectures and tutorials in the course, and implement either one of the following major job:

<!-- Please fill in "x" to replace the blank space between "[]" to tick the todo item; it's ticked on the first one by default. -->

- [x] **Application with Database System(s)**
- [ ] **Implementation of a Database System**

## Team Members

Our team consists of the following members, listed in the table below (the team leader is shown in the first row, and is marked with 🚩 behind his/her name):

<!-- change the info below to be the real case -->

| Student ID | Student Name | GitHub Account (in Email) | GitHub username |
| ---------- | ------------ | ------------------------- |-----------------|
| 118010246  | 秦兰 🚩      | 118010246@link.cuhk.edu.cn|[@QinLan18](https://github.com/QinLan18)        |
| 120090564  | 魏诗云       | 120090564@link.cuhk.edu.cn| [@Jane-912](https://github.com/Jane-912)        |
| 119010445  | 张新宇       | 119010445@link.cuhk.edu.cn| [@Zxy119010445](https://github.com/Zxy119010445) |
| 120090171  | 张梦瑶       | 120090171@link.cuhk.edu.cn| [@Exxcbt](https://github.com/Zmysjwgj)       |
| 120090702  | 李亿芊       | 120090702@link.cuhk.edu.cn| [@Lee-7102](https://github.com/Lee-7102)       |
| 120090322  | 陈琳         | 120090322@link.cuhk.edu.cn| [@iaaaaaamgood](https://github.com/iaaaaaamgood) |

## Project Specification

<!-- You should remove the terms/sentence that is not necessary considering your option/branch/difficulty choice -->

After thorough discussion, our team made the choice and the specification information is listed below:

- Our option choice is: **Option 1**
- Our branch choice is: **Branch 1**
- The difficulty level is: **Normal**


Our project structure and implementation can be found in [material/todo-list.md](./material/todo-list.md).
## Project Abstract
> <font size = 4>Here is the main structure of our designed database：</font>
### 1. Major Functionalities
- Register the package information that is 
released by some consumer
- Allow the consumer to appoint some plant for 
some package manually
- The assignment and the start-time of some 
operation with some machine could be further set 
under the constraint of plant appointment
- Once some operation is successfully finished, 
the processing record in end-time and expense 
could be written back.
- The production information, like manufacture 
capacity of some plant, or the demand changes of 
some consumer within some period of time can be 
calculated.
- Construct a bank system for consumers to complete their payments to the plant owner. Meanwhile, both consumers and plant owners can check their account balance through system websites.
<br></br>

### 2. Function Assumption
> <font size = 3.5>Request:</font>
- Relation between consumer and package possession:  
one-to-many relation  
One consumer can have multiple packages.

- Random allocation:  
If consumer doesn't appoint plant, our system will allocate one plant 
for him.

- Relation between packages and chips:
one-to-one relation  
One package refers to one type of chip. 

> <font size = 3.5>Production:</font> 
- Relation between plant and machine types:  
One plant holds one to many machines of the same type.

- No parallism for a single machine:  
One machine can process one operation at the same time.

- Relation between operation type and plant:  
One operation in a package can be assigned to only one plant.

- Consistency of plants for a single package:  
All processes(operations) of one package will be finished in the same plant, which means that the machine type of this plant will change after all chips finishes some process(operation).

> <font size = 3.5>Output:</font>
- Processing record:  
Processing record involves the start time, end time and expense of 
one operation processed on one machine.

- Waiting condition(test for demands):  
If all the plants are busy at certain time period, packages will be 
put in the waiting list. As soon as there is a free plant, package will be appointted.  

> <font size = 3.5>Possession and bank system:</font>
- Relation between plant and plant owners:  
A plant can belong to only one plant owner, but one plant owner could 
have multiple plants. 

- Both the consumer and the plant owner both has (for simplification, 
only one) bank account.
<br></br>

> <font size = 4>### 3. Schema Design: Chip Manufacture (__need to polish!!!__)</font>
#### (1)Chip Manufacture (__need to polish!!!__)
> Entity Sets

+ __consumer__(<u>consumer_ID</u>, package_ID)

+ __plant__(<u>plant_ID</u>, plant_name, machine_ID)

+ __package__(<u>package_ID</u>, consumer_ID, plant_ID, chip_Type, 
chip_Num, overall_time, expense_budget)

+ __operation_type__(operation_ID, precedency)

+ __machine__(<u>machine_ID</u>, machine_Type, plant_ID, feasibility)

+ __chip_type__(<u>chip_Type</u>, operation_id)

+ *__handle_record__*(<u>package_ID</u>, start_Time, end_Time, 
expense)

+ *__proc_record__*(<u>package_ID</u>, <u>operation_Type</u>, 
<u>machine_ID</u>, start_time, end_time, expense)
<br></br>


> Relationship

+ __consumer_appoint_plant__(<u>consumer_ID</u>, 
<u>package_ID</u>)

+ __plant_pocess_machine__(<u>plant_ID</u>,
<u>machine_ID</u>)

+ __machine_on_operation__(<u>machine_ID</u>,<u>operation_ID</u>, 
feasibility, running_time, expense)

+ __chip_require_operation__(<u>chip_Type</u>, <u>operation_id</u>)

<br></br>

#### (2) Bank System

+ Entity

    __consumer__(account_ID, passward, balance)
    __plant_owner__(account_ID, passward, balance)

+ Relationship

    __Payment__(<u>consumer.account_ID</u>,<u>plant_owner.account_ID</u>)

<br></br>

## ER Diagram(need be replaced soon later)
![image](https://user-images.githubusercontent.com/83419532/204967932-d6405bfc-a35a-4663-a913-5ef5928cd434.png)
<br></br>

