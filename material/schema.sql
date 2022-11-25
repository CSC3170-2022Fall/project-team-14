DROP SCHEMA IF EXISTS Chip;
CREATE SCHEMA IF NOT EXISTS Chip DEFAULT CHARACTER SET utf8;

USE Chip;

DROP TABLE IF EXISTS Consumer;
DROP TABLE IF EXISTS Plant_owner;
DROP TABLE IF EXISTS Plant;
DROP TABLE IF EXISTS Operation;
DROP TABLE IF EXISTS Machine_type;
DROP TABLE IF EXISTS Machine;
Drop TABLE IF EXISTS Packages;

CREATE TABLE Consumer(
    consumer_id varchar(20) NOT NULL,
    password varchar(50) NOT NULL,
    PRIMARY KEY (consumer_id)
);
CREATE TABLE Plant_owner(
    owner_id varchar(20) NOT NULL,
    password varchar(50) NOT NULL,
    plant_id varchar(50) NOT NULL,
    PRIMARY KEY (owner_id)
);
CREATE TABLE Plant(
    plant_id varchar(50) NOT NULL,
    type_name varchar(50) NOT NULL,
    income float(8,2),
    PRIMARY KEY (plant_id)
    -- FOREIGN KEY (type_name) REFERENCES Machine_type(type_name)
);
CREATE TABLE Operation(
    operation_type varchar(20) NOT NULL,
    time float(8,2) NOT NULL,
    expense float(8,2) NOT NULL,
    PRIMARY KEY (operation_type)
);
CREATE TABLE Machine_type(
    type_name varchar(50) NOT NULL,
    quota int NOT NULL,
    PRIMARY KEY (type_name)
);
CREATE TABLE Machine(
    machine_id varchar(50) NOT NULL,
    operation_type varchar(20) NOT NULL,
    status varchar(10),
    PRIMARY KEY (machine_id)
);
CREATE TABLE Packages(
    package_id varchar(50) NOT NULL,
    chip_number int NOT NULL,
    PRIMARY KEY (package_id)
);