set global log_bin_trust_function_creators = 1;
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

USE Chip;

-- --------------------------------------------------------

--
-- Dumping data for table `Consumer`
-- WAIT FOR insertion
--

INSERT INTO `Consumer` (`consumer_id`, `password`, `balance`) VALUES

-- --------------------------------------------------------

--
-- Dumping data for table `Plant_owner`
-- WAIT FOR insertion（这里演示的时候我们应该已经把plant_owner信息都注册好了）

DROP PROCEDURE IF EXISTS `insert_plant_owner`
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
DROP PROCEDURE IF EXISTS `own_info`
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
DROP PROCEDURE IF EXISTS `machine_info`
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

CALL `machine_info`(20);
SELECT count(*) FROM `machine_info`;
INSERT INTO `Machine` SELECT * FROM `machine_info`;

-- --------------------------------------------------------

--
-- Dumping data for table `Operation_machine_cost`
--

DROP PROCEDURE IF EXISTS `peration_machine`
CREATE PROCEDURE `insert_machine_operation`(IN n INT)
BEGIN
    opList = ['design-import', 'etch', 'bond', 'drill', 'test']
    DECLARE i INT DEFAULT 1;
    DECLARE machine_id INT DEFAULT 0;
    DECLARE operation_type varchar DEFAULT 0;
    DECLARE time FLOAT(8,2) DEFAULT 0;
    DECLARE expense FLOAT(8,2) DEFAULT 0;
    WHILE i <0 DO
        
        INSERT INTO `insert_plant_owner` VALUES(owner_id
        SET i = i+1;
    END WHILE;
END
INSERT INTO `Operation_machine_cost` (`machine_id`, `operation_type`, `time`, `expense`) VALUES


-- --------------------------------------------------------

--
-- Dumping data for table `Packages`
--

INSERT INTO `Packages` (`package_id`, `chip_number`, `chip_type`, `plant_id`, `consumer_id`, `total_expense`, `price`) VALUE

-- --------------------------------------------------------

--
-- Dumping data for table `Process_record`
--

INSERT INTO `Process_record` (`package_id`, `operation_type`, `machine_id`, `start_time`, `end_time`, `plant_id`, `status`) VALUES

-- --------------------------------------------------------

-- Dumping data for table `Chip_requires_operation`
--

INSERT INTO `Chip_requires_operation` (`chip_type`, `operation_type`, `precedency`, `expense`)

-- --------------------------------------------------------

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
--啊啊啊啊啊啊啊啊啊啊--