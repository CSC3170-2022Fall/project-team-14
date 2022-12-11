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
INSERT `Plant_owner`(`owner_id`,`password`) VALUES
("Qin Lan","123456"),
("Zhang Xinyu","654321"),
("Li Xianyi","123654");
-- --------------------------------------------------------

--
-- Dumping data for table `Own`
--
INSERT `Own`(`plant_id`,`owner_id`,`income`) VALUES
(1,"Qin Lan",0),
(2,"Qin Lan",0),
(3,"Qin Lan",0),
(4,"Qin Lan",0),
(5,"Qin Lan",0),
(6,"Qin Lan",0),
(7,"Zhang Xinyu",0),
(8,"Zhang Xinyu",0),
(9,"Zhang Xinyu",0),
(10,"Li Xianyi",0),
(11,"Li Xianyi",0),
(12,"Li Xianyi",0);
-- -------------------------------------------------------

--
-- Dumping data for table `Machine`
INSERT `Machine`(`machine_id`,`plant_id`,`operation_type`,`status`,`quota`) VALUES
(1,1,NULL,"IDLE",10000),
(2,12,NULL,"IDLE",20000),
(3,10,NULL,"IDLE",30000),
(4,7,NULL,"IDLE",50000),
(5,6,NULL,"IDLE",10500),
(6,4,NULL,"IDLE",26000),
(7,2,NULL,"IDLE",20000),
(8,4,NULL,"IDLE",18000),
(9,3,NULL,"IDLE",16000),
(10,2,NULL,"IDLE",20400),
(11,5,NULL,"IDLE",20000),
(12,8,NULL,"IDLE",20600),
(13,9,NULL,"IDLE",10600),
(14,1,NULL,"IDLE",10800),
(15,2,NULL,"IDLE",19000),
(16,6,NULL,"IDLE",18500),
(17,11,NULL,"IDLE",17000),
(18,9,NULL,"IDLE",14000),
(19,8,NULL,"IDLE",16000),
(20,7,NULL,"IDLE",20000);

-- --------------------------------------------------------

--
-- Dumping data for table `Operation_machine_cost`
--
INSERT `Operation_machine_cost`(`machine_id`,`operation_type`,`time`,`expense`) VALUES
(1,"design-import",10,10),
(1,"etch",15,15),
(1,"bond_A",13,15),
(1,"bond_B",12,12),
(1,"drill_A",12,12),
(1,"drill_B",12,12),
(1,"test",10,10),
(2,"design-import",5,5),
(2,"etch",10,10),
(2,"bond_A",8,8),
(2,"drill_A",12,12),
(2,"test",7,7),
(3,"design-import",8,8),
(3,"etch",15,15),
(3,"bond_A",20,20),
(3,"bond_B",12,12),
(3,"drill_A",18,18),
(3,"drill_B",12,12),
(3,"test",10,10),
(4,"design-import",7,7),
(4,"etch",15,15),
(4,"bond_A",10,10),
(4,"drill_A",12,12),
(4,"test",6,6),
(5,"design-import",5,5),
(5,"etch",15,15),
(5,"bond_A",15,15),
(5,"bond_B",12,12),
(5,"drill_A",15,15),
(5,"drill_B",12,12),
(5,"test",10,10),
(6,"design-import",12,12),
(6,"etch",15,15),
(6,"bond_A",13,13),
(6,"drill_A",12,12),
(6,"test",10,10),
(7,"design-import",10,10),
(7,"etch",15,15),
(7,"bond_A",13,15),
(7,"bond_B",12,12),
(7,"drill_A",12,12),
(7,"drill_B",12,12),
(7,"test",10,10),
(8,"design-import",10,10),
(8,"etch",15,15),
(8,"bond_A",13,15),
(8,"bond_B",12,12),
(8,"drill_A",12,12),
(8,"drill_B",12,12),
(8,"test",10,10),
(9,"design-import",10,10),
(9,"etch",15,15),
(9,"bond_A",13,15),
(9,"bond_B",12,12),
(9,"drill_A",12,12),
(9,"test",10,10),
(10,"design-import",10,10),
(10,"etch",15,15),
(10,"bond_A",13,15),
(10,"bond_B",12,12),
(10,"drill_A",12,12),
(10,"drill_B",12,12),
(10,"test",10,10),
(11,"design-import",10,10),
(11,"etch",15,15),
(11,"bond_A",13,15),
(11,"bond_B",12,12),
(11,"drill_A",12,12),
(11,"drill_B",12,12),
(11,"test",10,10),
(12,"design-import",10,10),
(12,"etch",15,15),
(12,"bond_A",13,15),
(12,"drill_A",12,12),
(12,"test",10,10),
(13,"design-import",10,10),
(13,"etch",15,15),
(13,"bond_A",13,15),
(13,"bond_B",12,12),
(13,"drill_A",12,12),
(13,"drill_B",12,12),
(13,"test",10,10),
(14,"design-import",10,10),
(14,"etch",15,15),
(14,"bond_A",13,15),
(14,"drill_A",12,12),
(14,"drill_B",12,12),
(14,"test",10,10),
(15,"design-import",10,10),
(15,"etch",15,15),
(15,"bond_A",13,15),
(15,"drill_A",12,12),
(15,"test",10,10),
(16,"design-import",10,10),
(16,"etch",15,15),
(16,"bond_A",13,15),
(16,"bond_B",12,12),
(16,"drill_A",12,12),
(16,"drill_B",12,12),
(16,"test",10,10),
(17,"design-import",10,10),
(17,"etch",15,15),
(17,"bond_A",13,15),
(17,"drill_A",12,12),
(17,"test",10,10),
(18,"design-import",10,10),
(18,"etch",15,15),
(18,"bond_A",13,15),
(18,"bond_B",12,12),
(18,"drill_A",12,12),
(18,"drill_B",12,12),
(18,"test",10,10),
(19,"design-import",10,10),
(19,"etch",15,15),
(19,"bond_A",13,15),
(19,"bond_B",12,12),
(19,"drill_A",12,12),
(19,"test",10,10),
(20,"design-import",10,10),
(20,"etch",15,15),
(20,"bond_A",13,15),
(20,"bond_B",12,12),
(20,"drill_A",12,12),
(20,"test",10,10);

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
INSERT `Chip_expense`(`chip_type`,`price`) VALUES
("a",10),
("b",15),
("c",20),
("d",25),
("e",30),
("f",35);

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