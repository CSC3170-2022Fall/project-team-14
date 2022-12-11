set global log_bin_trust_function_creators = 1;
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

USE Chip;

-- --------------------------------------------------------

--
-- Dumping data for table `Consumer`
-- WAIT FOR insertion


-- --------------------------------------------------------

--
-- Dumping data for table `Plant_owner`
-- WAIT FOR insertion

DROP PROCEDURE IF EXISTS `insert_plant_owner`;
CREATE PROCEDURE `insert_plant_owner`(IN n INT)
BEGIN
    $LISTBUILD("Qin Lan","Zhang Xinyu","Li Qianyi","Wei Shiyun","Zhang Mengyao","Emily","TOM","JERRY") AS `owner_list`;
    DECLARE i INT DEFAULT 1;
    DECLARE `owner_id` INT DEFAULT 0;
    DECLARE `owner_name` VARCHAR(20) DEFAULT " ";
    DECLARE `password` INT DEFAULT 0;
    WHILE i < n DO
        SET `owner_id` = i;
        SET `owner_name` = $LIST(`owner_list`,i);
        SET `password` = FLOOR(RAND()*100000);
        INSERT INTO `insert_plant_owner` VALUES(`owner_id`, `owner_name`,`password`);
        SET i = i+1;
    END WHILE;
END;

CALL `insert_plant_owner`(8);
SELECT count(*) FROM `insert_plant_owner`;
INSERT INTO `plant_owner` SELECT * FROM `insert_plant_owner`;

-- --------------------------------------------------------

--
-- Dumping data for table `Own`
--
DROP PROCEDURE IF EXISTS `own_info`;
CREATE PROCEDURE `own_info`(IN n INT)
BEGIN
    DECLARE i INT DEFAULT 1;
    DECLARE `plant_id` INT DEFAULT 0;
    DECLARE `owner_id` INT DEFAULT 1;
    DECLARE `UPPER` INT;
    SET `UPPER` = 12;
    DECLARE `LOWER` INT;
    SET `LOWER` = 1;
    DECLARE `income` float(8,2) DEFAULT 0;
    WHILE i < n DO
        SET `plant_id` = i;
        SET `owner_id` = ROUND(((`UPPER`-`LOWER`-1)*RAND()+`LOWER`),0);
        INSERT INTO `own_info` VALUES(`plant_id`,`owner_id`,`income`);
        set i = i+1;
    END WHILE;
END;

CALL `own_info`(12);
SELECT count(*) FROM `own_info`;
INSERT INTO `Own` SELECT * FROM `own_info`;

-- -------------------------------------------------------

--
-- Dumping data for table `Machine`
--
DROP PROCEDURE IF EXISTS `machine_info`;
CREATE PROCEDURE `machine_info`(IN n INT)
BEGIN
    DECLARE i INT DEFAULT 1;
    DECLARE `machine_id` DEFAULT 1;
    DECLARE `plant_id` DEFAULT 1;
    DECLARE `UPPER` INT;
    SET `UPPER` = 12;
    DECLARE `LOWER` INT;
    SET `LOWER` = 1;
    DECLARE `status` varchar(20) DEFAULT 'Finished';
    DECLARE `quota` int DEFAULT 0;
    WHILE i < n DO
        SET `machine_id` = i;
        SET `plant_id` = ROUND(((`UPPER`-`LOWER`-1)*RAND()+`LOWER`),0);
        SET `quota` = ROUND(100+RAND()*100);
        INSERT INTO `machine_info` VALUES(`machine_id`,`plant_id`,`status`,`quota`);
        SET i = i+1;
    END WHILE;
END;

CALL `machine_info`(50);
SELECT count(*) FROM `machine_info`;
INSERT INTO `Machine` SELECT * FROM `machine_info`;

-- --------------------------------------------------------

--
-- Dumping data for table `Operation_machine_cost`
--

DROP PROCEDURE IF EXISTS `operation_machine_info`;
CREATE PROCEDURE `operation_machine_info`(IN n INT)
BEGIN
    $LISTBUILD('design-import', 'etch_A', 'etch_B', 'bond_A','bond_B' 'drill', 'test') AS opList;
    DECLARE i INT DEFAULT 1; --# of machine:50-- 
    DECLARE j INT DEFAULT 1; --index of the operation--
    DECLARE machine_id INT DEFAULT 1;
    DECLARE operation_type varchar DEFAULT 0;
    DECLARE time FLOAT(8,2) DEFAULT 0;
    DECLARE expense FLOAT(8,2) DEFAULT 0;
    WHILE i <n DO
        while j<8 DO
            SET `machine_id` = i;
            SET `operation_type` = $LIST(`oplist`,j);
            SET `time` = RAND()*10  --time per unit chip per operation
            SET `expense` = RAND() --expense per unit chip per operation
            SET j = j+1;
        SET i = i+1;
    END WHILE;
END;

CALL `operation_machine_info`(50);
SELECT count(*) FROM `operation_machine_info`;
INSERT INTO `Operation_machine_cost` SELECT * FROM `operation_machine_info`;

-- --------------------------------------------------------

--
-- Dumping data for table `Packages`
--

-- --------------------------------------------------------

--
-- Dumping data for table `Process_record`
--

-- --------------------------------------------------------

--
-- Dumping data for table `Chip_expense`
--
DROP PROCEDURE IF EXISTS `chip_expense_info`;
CREATE PROCEDURE `chip_expense_info`(IN n INT) -- # of chip types = 6--
BEGIN
    $LISTBUILD("A","B","C","D","E","F") AS `type_list`;
    DECLARE i INT DEFAULT 1;
    DECLARE `chip_type` varchar(20) DEFAULT " ";
    DECLARE `price` float(8,2) DEFAULT;
    WHILE i<n DO
        SET `chip_type` = $LIST(`type_list`,i);
        SET `price` = RAND()*10000;
        SET i = i+1;
    END WHILE;
END;

CALL`chip_expense_info`(6);
SELECT count(*) FROM `chip_expense_info`;
INSERT INTO `Chip_expense` SELECT * FROM `chip_expense_info`;


-- --------------------------------------------------------
--
-- Dumping data for table `Chip_requires_operation`
--
INSERT `Chip_requires_operation`(`chip_type`,`operation_type`,`precedency`) VALUES
("A", "design-import", 0),
("A", "etch_A",1),
("A","etch_B",2),
("A","bond_A",3),
("A","bond_B",4),
("A","drill",5),
("A","test",6),
("B", "design-import", 0),
("B", "etch_A",1),
("B","etch_B",2),
("B","bond_A",3),
("B","bond_B",4),
("B","drill",5),
("B","test",6),
("C", "design-import", 0),
("C", "etch_A",1),
("C","etch_B",2),
("C","bond_A",3),
("C","bond_B",4),
("C","drill",5),
("C","test",6),
("D", "design-import", 0),
("D", "etch_A",1),
("D","etch_B",2),
("D","bond_A",3),
("D","bond_B",4),
("D","drill",5),
("D","test",6),
("E", "design-import", 0),
("E", "etch_A",1),
("E","etch_B",2),
("E","bond_A",3),
("E","bond_B",4),
("E","drill",5),
("E","test",6),
("F", "design-import", 0),
("F", "etch_A",1),
("F","etch_B",2),
("F","bond_A",3),
("F","bond_B",4),
("F","drill",5),
("F","test",6);

-- --------------------------------------------------------

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
-- 啊啊啊啊啊啊啊啊啊啊--