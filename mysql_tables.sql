-----------------------------------------------------------------------------
---------------------- Create table to store Results ------------------------
------------- Make these Tables in upboard DB or modify script.py code ------
-----------------------------------------------------------------------------


CREATE TABLE `studentsubjects10th` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rollno` bigint(20) DEFAULT NULL,
  `subjects` varchar(255) DEFAULT NULL,
  `mark` varchar(255) DEFAULT NULL,
  `practical` varchar(255) DEFAULT NULL,
  `total` varchar(255) DEFAULT NULL,
  `grade` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `rollno` (`rollno`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci




CREATE TABLE `studentinfo10th` (
  `rollno` bigint(20) NOT NULL,
  `name` text NOT NULL,
  `father` text NOT NULL,
  `mother` text NOT NULL,
  `dob` varchar(255) NOT NULL,
  PRIMARY KEY (`rollno`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
