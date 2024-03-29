
DROP SCHEMA IF EXISTS Chip;
CREATE SCHEMA IF NOT EXISTS Chip DEFAULT CHARACTER SET utf8;

USE Chip;

DROP TABLE IF EXISTS Consumer;
DROP TABLE IF EXISTS Plant_owner;
DROP TABLE IF EXISTS Own;
DROP TABLE IF EXISTS Machine;
DROP TABLE IF EXISTS Operation_machine_cost;
DROP TABLE IF EXISTS Packages;
DROP TABLE IF EXISTS Process_record;
DROP TABLE IF EXISTS Chip_expense;
DROP TABLE IF EXISTS Chip_requires_operation;

CREATE TABLE `Consumer`(
    `consumer_id` varchar(20) NOT NULL,
    `password` varchar(1500) NOT NULL,
    `balance` float(10,2) DEFAULT 0.00,
    PRIMARY KEY (`consumer_id`)
);
CREATE TABLE `Plant_owner`(
    `owner_id` varchar(20) NOT NULL,
    `password` varchar(1500) NOT NULL,
    PRIMARY KEY (`owner_id`)
);
CREATE TABLE `Own`(
    `plant_id` INT NOT NULL,
    `owner_id` varchar(20) NOT NULL,
    `income` float(8,2),
    PRIMARY KEY (`plant_id`)
);

CREATE TABLE `Machine`(
    `machine_id` INT NOT NULL,
    `plant_id` INT NOT NULL,
    `operation_type` varchar(20) DEFAULT NULL,
    `status` varchar(20) DEFAULT "IDLE",
    `quota` int NOT NULL,
    PRIMARY KEY (`machine_id`)
    -- FOREIGN KEY (plant_id) REFERENCES Own(plant_id)
);
CREATE TABLE `Operation_machine_cost`(
    `machine_id` INT NOT NULL,
    `operation_type` varchar(20) DEFAULT "None",
    `time` INT NOT NULL,
    `expense` float(8,2) NOT NULL,
    PRIMARY KEY (`machine_id`, `operation_type`)
);
CREATE TABLE `Packages`(
    `package_id` INT NOT NULL,
    `chip_number` INT NOT NULL,
    `chip_type` varchar(20) NOT NULL,
    `plant_id` INT NOT NULL,
    `consumer_id` varchar(20) NOT NULL,
    `total_expense` float(8,2) NOT NULL DEFAULT 0.00,
    `price` float(8,2) NOT NULL,
    PRIMARY KEY (`package_id`)
    -- FOREIGN KEY (plant_id) REFERENCES Own(plant_id),
    -- FOREIGN KEY (consumer_id) REFERENCES Consumer(consumer_id)
);

CREATE TABLE `Process_record`(
    `package_id` INT NOT NULL,
    `operation_type`varchar(20) NOT NULL,
    `machine_id` INT NOT NULL,
    `start_time` INT NOT NULL,
    `end_time` INT NOT NULL,
    `plant_id` INT NOT NULL,
    `status` varchar(20),
    PRIMARY KEY (`package_id`, `operation_type`, `machine_id`)
    -- FOREIGN KEY (plant_id) REFERENCES Own(plant_id)
);
CREATE TABLE `Chip_expense`(
    `chip_type` varchar(20) NOT NULL,
    `price` float(8,2) NOT NULL,
    PRIMARY KEY (`chip_type`)
);
CREATE TABLE `Chip_requires_operation`(
    `chip_type` varchar(20) NOT NULL,
    `operation_type` varchar(20) NOT NULL,
    `precedency` int NOT NULL DEFAULT 0,
    PRIMARY KEY (`chip_type`, `operation_type`)
);
                                        

INSERT `Packages`(`package_id`,`chip_number`,`chip_type`,`plant_id`,`consumer_id`,`total_expense`,`price`) VALUES
(1,3,"a",1,1,55,66),
(2,3,"a",1,1,55,66),
(3,3,"a",1,1,55,66);
INSERT INTO `Process_record`(`package_id`, `operation_type`, `machine_id`, `start_time`, `end_time`, `plant_id`, `status`) VALUES
(1,"design-import",3,4,5,1,"OCCUPIED"),
(2,"drill",2,3,5,1,"OCCUPIED"),
(3,"bound_B",1,2,5,1,"OCCUPIED");

