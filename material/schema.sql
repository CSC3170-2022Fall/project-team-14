DROP SCHEMA IF EXISTS Chip;
CREATE SCHEMA IF NOT EXISTS Chip DEFAULT CHARACTER SET utf8;

USE Chip;

DROP TABLE IF EXISTS Consumer;
DROP TABLE IF EXISTS Plant_owner;
DROP TABLE IF EXISTS Own;
DROP TABLE IF EXISTS Machine_type;
DROP TABLE IF EXISTS Machine;
DROP TABLE IF EXISTS Operation_machine_cost;
DROP TABLE IF EXISTS Packages;
DROP TABLE IF EXISTS Handler_record;
DROP TABLE IF EXISTS Process_record;
DROP TABLE IF EXISTS Chip_requires_operation;

CREATE TABLE Consumer(
    consumer_id varchar(20) NOT NULL,
    password varchar(50) NOT NULL,
    PRIMARY KEY (consumer_id)
);
CREATE TABLE Plant_owner(
    owner_id varchar(20) NOT NULL,
    password varchar(50) NOT NULL,
    PRIMARY KEY (owner_id)
);
CREATE TABLE Own(
    plant_id varchar(50) NOT NULL,
    owner_id varchar(20) NOT NULL,
    type_name varchar(50) NOT NULL,
    income float(8,2),
    PRIMARY KEY (plant_id, owner_id)
    -- FOREIGN KEY (type_name) REFERENCES Machine_type(type_name),
    -- FOREIGN KEY (owner_id) REFERENCES Plant_owner(owner_id)
);
CREATE TABLE Machine_type(
    type_name varchar(50) NOT NULL,
    quota int NOT NULL,
    PRIMARY KEY (type_name)
);
CREATE TABLE Machine(
    machine_id varchar(50) NOT NULL,
    plant_id varchar(50) NOT NULL,
    operation_type varchar(20) NOT NULL,
    status varchar(10),
    PRIMARY KEY (machine_id)
    -- FOREIGN KEY (plant_id) REFERENCES Plant(plant_id)
);
CREATE TABLE Operation_machine_cost(
    machine_id varchar(50) NOT NULL,
    operation_type varchar(20) NOT NULL,
    time float(8,2) NOT NULL,
    expense float(8,2) NOT NULL,
    PRIMARY KEY (machine_id, operation_type)
);
CREATE TABLE Packages(
    package_id varchar(50) NOT NULL,
    chip_number int NOT NULL,
    chip_type varchar(20) NOT NULL,
    plant_id varchar(50) NOT NULL,
    consumer_id varchar(20) NOT NULL,
    PRIMARY KEY (package_id)
    -- FOREIGN KEY (plant_id) REFERENCES Plant(plant_id),
    -- FOREIGN KEY (consumer_id) REFERENCES Consumer(consumer_id)
);
CREATE TABLE Handler_record(
    package_id varchar(50) NOT NULL,
    start_time TIMESTAMP NOT NULL DEFAULT now(),
    end_time TIMESTAMP NOT NULL,
    expense float(8,2) NOT NULL,
    plant_id varchar(50) NOT NULL,
    PRIMARY KEY (package_id)
    -- FOREIGN KEY (plant_id) REFERENCES Plant(plant_id)
);
CREATE TABLE Process_record(
    package_id varchar(50) NOT NULL,
    operation_type varchar(20) NOT NULL,
    machine_id varchar(50) NOT NULL,
    start_time TIMESTAMP NOT NULL DEFAULT now(),
    end_time TIMESTAMP NOT NULL,
    expense float(8,2) NOT NULL,
    PRIMARY KEY (package_id, operation_type, machine_id)
);
CREATE TABLE Chip_requires_operation(
    chip_type varchar(20) NOT NULL,
    operation_type varchar(20) NOT NULL,
    precedency int NOT NULL DEFAULT 0,
    PRIMARY KEY (chip_type, operation_type)
);
