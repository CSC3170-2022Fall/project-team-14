## Remark
- any words followed '()' is a button / function, inside '()' are input variables
- if without '()', they are just variables that need to show 

## 1.log in page
- login_plant_owner(username, password) -> 7.plant_owner home page
- login_customer(username, password) -> 3. customer home page
- register() -> 2. register page

## 2.register page
- register(username, password, password2) -> 1. log in page    // need to check if 2 passwords equal
  
## 3.customer home page
- package_id, chip_type, chip_number, status, start_time, end_time, expense
- register_package() -> 4.register package page

## 4.register package page
- register(chip_type, chip_number, plant_id) -> 5.pay page    //chip_type and plant_id will be limitted

## 5.pay page
- expense, balance 
- pay() -> 6.return page    // need to check if balance >= expense

## 6.return page
- return() ->3.customer home page 

## 7.plant_owner home page
- package_id, chip_type, chip_number, customer_id, start_time, status    // status = operation_type or finished or waiting
- machine_id, status    // status = operation_type or idle
- change_start_time(machine_id, start_time, operation_type) -> 7.plant_owner home page self-refresh



  
