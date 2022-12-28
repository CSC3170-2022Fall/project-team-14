[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=9422486&assignment_repo_type=AssignmentRepo)
# CSC3170 Course Project

## 1. Project Overall Description

This is our implementation for the course project of CSC3170, 2022 Fall, CUHK(SZ). For details of the project, you can refer to [project-description.md](project-description.md). In this project, we will utilize what we learned in the lectures and tutorials in the course, and implement either one of the following major job:

<!-- Please fill in "x" to replace the blank space between "[]" to tick the todo item; it's ticked on the first one by default. -->

- [x] **Application with Database System(s)**
- [ ] **Implementation of a Database System**

## 2. Team Members

Our team consists of the following members, listed in the table below (the team leader is shown in the first row, and is marked with 🚩 behind his/her name):

<!-- change the info below to be the real case -->

| Student ID | Student Name | GitHub Account (in Email) | GitHub username |
| ---------- | ------------ | ------------------------- |-----------------|
| 118010246  | 秦兰 🚩      | 118010246@link.cuhk.edu.cn|[@QinLan18](https://github.com/QinLan18)        |
| 120090564  | 魏诗云       | 120090564@link.cuhk.edu.cn| [@Jane-912](https://github.com/Jane-912)        |
| 119010445  | 张新宇       | 119010445@link.cuhk.edu.cn| [@Zxy119010445](https://github.com/Zxy119010445) |
| 120090171  | 张梦瑶       | 120090171@link.cuhk.edu.cn| [@Exxcbt](https://github.com/Zmysjwgj)       |
| 120090702  | 李亿芊       | 120090702@link.cuhk.edu.cn| [@Lee-7102](https://github.com/Lee-7102)       |
| 120090322  | 陈琳         | 120090322@link.cuhk.edu.cn| [@EMILYcodingVer](https://github.com/EMILYcodingVER)   |

## 3. Project Specification

<!-- You should remove the terms/sentence that is not necessary considering your option/branch/difficulty choice -->

After thorough discussion, our team made the choice and the specification information is listed below:

- Our option choice is: **Option 1**
- Our branch choice is: **Branch 1**
- The difficulty level is: **Normal**

## 4. Repository Structure

- .github
- .venv (the virtual environment for flask running)
- .vscode (connects the VScode)
- App (contains our project code, the compile instruction is in the [App/readme.md](./App/readme.md))
- material (contains outline, to-do list and page_structure)
    - [Chip Manufacture.xmind](./material/Chip%20Manufactuer.xmind): outline
    - [material/todo-list.md](./material/todo-list.md): our work distribution and implementation.
    - [page_structure.md](./material/page_structure.md): the name of values in the form, through which connect the frond end and back end.
- [project-description.md](project-description.md) (shows details of every option, you can see Option1-Branch1-Normal for details)

## 4. Project
> ### Project abstract
The main goal of our project is to implement an application with a database system, which aims to assign chip manufacturing orders to different plants in real time. We predefined and randomly created some data types to simulate the realistic order information. Our implementation consists of transferring input data into the database, designing data storage modules, designing order distribution algorithms and creating web pages to realize user interaction and display production states for both order holders and plant owners. The final achievements is that:

For plant owners, after logging into the home page, he has access to the production information of plants he manages, information consisting of plant_id, order_id, start_production_time, expected_end_time which belongs to the order on process,etc.

For order holders, after logging into the home page, he can visit the production information of his own order, information consisting of plant_id which this order belongs to,  start_time and expected_end_time if this order is under production, the total prices he needs to pay,etc.

The highlights of our project is that, besides the complete front and back-end data updating system and intuitive web design, we also have a set of distribution algorithms to manage the input orders in real time, for example, creating a waiting space when orders overflow. 

> ### Introduction
### (1) Major Functionalities
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

### (2) Function Assumption
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

> ### Schema Design
We design our database structure from two aspects: consumer and plant owner. The consumer registers packages and can see the process record. The plant owner owns plants, has machines, and can see process record. Relating to the machine entity, it has one to many relation with operation, and the operation has many to one relation with chip.
#### (i) Chip Manufacture
> Entity Sets

+ __consumer__(<u>consumer_ID</u>, password, balance)

+ __plant_owner__(<u>owner_ID</u>, password)

+ __owner__(<u>plant_ID</u>, owner_id, income)

+ __packages__(<u>package_ID</u>, consumer_ID, plant_ID, chip_Type, 
chip_Num, total_expense, price)

+ __operation__(operation_Type, feasibility)

+ __machine__(<u>machine_ID</u>, machine_Type, plant_ID, feasibility)

+ __chip__(<u>chip_Type</u>, precedency)

+ __proc_record__(<u>package_ID</u>, <u>operation_Type</u>, 
<u>machine_ID</u>, start_time, end_time, plant_id, status)
<br></br>


> Relationship

+ __operation_machine_cost__(<u>machine_ID</u>,<u>operation_Type</u>, time, expense)

+ __chip_require_operation__(<u>chip_Type</u>, <u>operation_Type</u>, precedency)


#### (ii) Bank System

> Entity

+ __consumer__(account_ID, passward, balance)
+ __plant_owner__(account_ID, passward, balance)

> Relationship

+ __Payment__(<u>consumer.account_ID</u>,<u>plant_owner.account_ID</u>)

Here is our ER-diagram: 
![image](https://user-images.githubusercontent.com/83419532/209425047-a1aea5ea-92dc-4076-82ae-605aaf9657d2.png)
<br></br>

we also completed some predefined data into [App/insert.sql](./App/insert.sql) . 
They are machine information,containing the number of machines and their maximum production quota,
chip types along with their selling prices and full operation steps,
the operation steps to produce a certain type of chip along with the spent time and expenses. 

> ### Algorithm
[App/alg.py](./App/alg.py) is about algorithms to handle tasks. There are four kinds of tasks. 
(1) Allocating one operation of a package: It will choose machines to handle the package, change machines’ working status, package record and calculate expense, estimated end time and actual end time. 
(2) Changing operation type: It will change one machine’s operation type at the time set by the plant owner if the machine is idle or as soon as it becomes idle.  
(3) Terminating one operation of a package: It will then calculate total income if the whole package is ended or put the package into queue again for next operation. 
(4) Terminating one operation of a machine: It will change process record to actual end time and machine’s status to idle .
All the tasks will be put into a priority queue with timestamps indicating when to handle them. When the function "search_call" is called, the program will execute tasks and update the database in the queue whose timestamps are smaller than the current time’s timestamp.
<br></br>

> ### Functionality implementation
> Consumer
When registering as a consumer, the consumer needs to enter the username, password and enter password a second time to check the correctness. The username and password are stored as consumer id in the “Consumer” table. 
![image](pics/image/%E5%9B%BE%E7%89%87%201.png)
![image](pics/image/%E5%9B%BE%E7%89%87%202.png)

After registering, the webpage will redirect to the login page. After log in, the home page of a new consumer will display a module for ordering new packages, a package list showing all packages for the consumer but empty for new consumers(Notice that for a new consumer after registering, he or she should have no packages), and a module for searching the condition of a certain package.
![image](pics/image/%E5%9B%BE%E7%89%87%203.png)

For the “Register your package” module, the consumer can choose a chip type for his or her package, and then enter a chip number. The consumer can either choose a certain available plant or does not choose it, which will be allocated by our system automatically. For chip number, the consumer should type it manually. For chip type and plant id, we display available ones in drop-down box form.

![image](pics/image/%E5%9B%BE%E7%89%87%204.png)
![image](pics/image/%E5%9B%BE%E7%89%87%205.png)

After choosing those three info, by clicking the “Register package” button, the consumer will be redirected to the payment page. 
![image](pics/image/%E5%9B%BE%E7%89%876.png)

The payment page will display the generated package id for this newly ordered package, the chip type, chip number, plant id and the price for this package. Also, it will show the balance for the consumer. The consumer should be able to find that his or her balance is not enough for paying this package if “price” is larger than “balance”. After that, the consumer can click the “Pay” button to finish the payment. If the payment is successful, the page will show a green warning: “Pay Success!” and the consumer will find that the balance has been updated. If the payment fails, the page will show a red warning: “Your balance is not available, payment fails.” The consumer can click the “Return” button to redirect back to the home page.
![image](pics/image/%E5%9B%BE%E7%89%87%207.png)
![image](pics/image/%E5%9B%BE%E7%89%87%208.png)

For the “Package List” module, it shows all the packages of a consumer by presenting their package id, chip type, chip number, plant id and price.
![image](pics/image/%E5%9B%BE%E7%89%87%2010.png)

For the “Package Details” module, it offers all the package ids in a drop-down box form as well, and the consumer can choose one package to check its detailed information, like the start time and status of each operation in this package.
![image](pics/image/%E5%9B%BE%E7%89%87%2011.png)
![image](pics/image/%E5%9B%BE%E7%89%87%2012.png)
![image](pics/image/%E5%9B%BE%E7%89%87%2013.png)
</br>

> Plant owner

When registering as a plant owner, the plant owner needs to enter the username, password and then select the plant id of his plant. The username is stored as plant owner id in the “Plant_owner” table, and the plant id chosen is stored as plant id in the “Own” table in the database. In our project, we assume the number of plants is specified in advance. When a plant owner registers, he needs to choose among those plant-ids. Therefore, we don’t need to deal with the problem that we need to specify the machines and operation types information of that plant. 

After registering, the web page will redirect to the login page. And after login in, the home page of the new registered plant owner displays all empty for package list, machine status, and change start time/operation type.

![image](pics/image/%E5%9B%BE%E7%89%87%2014.png)
![image](pics/image/%E5%9B%BE%E7%89%87%2015.png)

When loging in as a plant owner, the plant owner needs to enter his username, password and then clicks “Login Plant” button. The homepage of the plant owner shows the package list, machine status, and change of start time and operation type. In the package list, there are package id, chip type, chip number, consumer, start time, and status. Its primary key is package id. The machine status displays the machine id, status, operation type, start time, and estimated end time. Its primary key is the joint of package id, operation type, and machine id. In the “change start time/operation type” module, it provides the machine id, start time, and operation type for the plant owner to choose a specific machine the plant owner wants to change. The machines are all from the owner’s plant and are displayed in the drop-down box form. The start time means the delayed time the owner wants to apply to the original start time. The operation type displays so in a drop-down box form.

![image](pics/image/%E5%9B%BE%E7%89%87%2016.png)
![image](pics/image/%E5%9B%BE%E7%89%87%2017.png)
![image](pics/image/%E5%9B%BE%E7%89%87%2018.png)
![image](pics/image/%E5%9B%BE%E7%89%87%2019.png)
![image](pics/image/%E5%9B%BE%E7%89%87%2020.png)

There are two ways to realize the change of operation type. The first method is a dynamic drop-down box, which means after choosing the machine id, the available operation type will be displayed in the operation type option. However, the web page will only be refreshed after the plant owner clicks the “Apply” button. If using this method, the pure usage of HTML code is not enough and routing to the HTML web page in the python scripts also needs to be modified. Therefore this method is given up.
The second method is that the operation type option displays all the operation types available for all machines. Then after the plant owner chooses the operation type, and clicks the “Apply” button, the request will be left to the back end. The back end will decide whether the operation type the plant owner chooses is available for the specific machine. If available, it will post success “Changed success” and redirect to the home page. If not, it will post an error "The operation type is not available, please choose again!" and redirect to the home page.

![image](pics/image/%E5%9B%BE%E7%89%87%2021.png)
![image](pics/image/%E5%9B%BE%E7%89%87%2022.png)



## 6. How to run
see [App/readme.md](./App/readme.md)

## 7. Presentation Video Link
https://www.bilibili.com/video/BV1rK411B7DX/?vd_source=3bfc39e790a51878aa96168dedff4ebf

## 8. Presentation slides
see [CSC3170_group14_slides.pdf](./CSC3170_group14_slides.pdf)