# Work Distribution
## 前期 - preparation
| Student ID | Student Name | Work                      |
| ---------- | ------------ | ------------------------- |
| 118010246  | 秦兰          | Web page(Frond end)       |       
| 119010445  | 张新宇        | Web page(Frond end)       |
| 120090322  | 陈琳          | Document edit             |
| 120090171  | 张梦瑶        | ER Diagram and schema     |
| 120090702  | 李亿芊        | Database(back end)        |
| 120090564  | 魏诗云        | Database(back end)        |

## 中期 - coding
| Student ID | Student Name | Work                      |
| ---------- | ------------ | ------------------------- |
| 118010246  | 秦兰          | Frond end - consumer page: [index_consumer.html](../App/templates/index_consumer.html); login page: [login.html](../App/templates/login.html)      |       
| 119010445  | 张新宇        | Frond end - plant owner page: [index_plant.html](../App/templates/index_plant.html); register page: [register_consumer.html](../App/templates/register_consumer.html) & [register_owner.html](../App/templates/register_owner.html)       |
| 120090322  | 陈琳          | Back end - insert data into database [insert.sql](../App/insert.sql)             |
| 120090171  | 张梦瑶        | Back end - [plant.py](../App/plant.py)     |
| 120090702  | 李亿芊        | Back end - algorithm: [alg.py](../App/alg.py)        |
| 120090564  | 魏诗云        | Back end - create database: [schema.sql](../App/schema.sql); [consumer.py](../App/consumer.py)        |

## 后期 - report, presentation and recording
| Student ID | Student Name | Work                      |
| ---------- | ------------ | ------------------------- |
| 118010246  | 秦兰          | report       |       
| 119010445  | 张新宇        | report       |
| 120090322  | 陈琳          | Presentation - part1           |
| 120090171  | 张梦瑶        | Presentation - part2    |
| 120090702  | 李亿芊        | report - Algorithm       |
| 120090564  | 魏诗云        | Record demo        |




# Implementation

## User Interface (frond end)

### register

register page
- [consumer reigster](../App/templates/register_consumer.html)
- [plant owner register](../App/templates/register_owner.html)

### consumer

1. [login page](../App/templates/login.html)
- account
- password

2. [home page](../App/templates/index_consumer.html)
- Register package information ( link to payment page)
- My package
    - package id
    - chip type
    - chip number
    - plant id
    - price

4. [payment](../App/templates/payment.html)
- success
- fail

    

### Plant owner 
1. login page
- account
- password
2. [home page](../App/templates/index_plant.html)
- Package list( finished and waiting list all shown)
    - machine ID
        - operation type (can be changed by plant owner)
        - start-time (plant owner can set the start-time, or the actual start-time will be shown)
        - estimated end-time
        - actual end-time
        - expense
    


## Database and algorithm (back end)

[app.py](../App/app.py) - for app running

[db.py](../App/db.py) - for database connecting

[auth.py](../App/auth.py) - for user register and login

[consumer.py](../App/consumer.py) - for consumer

[plant.py](../App/plant.py) - for plant owner

[alg.py](../App/alg.py) - implement package allocating


