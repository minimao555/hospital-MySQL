/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50726
 Source Host           : localhost:3306
 Source Schema         : hospital

 Target Server Type    : MySQL
 Target Server Version : 50726
 File Encoding         : 65001

 Date: 10/10/2022 23:04:16
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for doctor
-- ----------------------------
DROP TABLE IF EXISTS `doctor`;
CREATE TABLE `doctor`  (
  `doctorID` char(10) CHARACTER SET utf8 COLLATE utf8_croatian_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_croatian_ci NOT NULL,
  `sex` enum('男','女') CHARACTER SET utf8 COLLATE utf8_croatian_ci NOT NULL DEFAULT '男',
  `age` int(255) NOT NULL,
  `phoneNumber` varchar(255) CHARACTER SET utf8 COLLATE utf8_croatian_ci NOT NULL,
  `address` varchar(255) CHARACTER SET utf8 COLLATE utf8_croatian_ci NOT NULL,
  `office` varchar(255) CHARACTER SET utf8 COLLATE utf8_croatian_ci NOT NULL,
  `photo` blob NOT NULL,
  PRIMARY KEY (`doctorID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_croatian_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for inspection_item
-- ----------------------------
DROP TABLE IF EXISTS `inspection_item`;
CREATE TABLE `inspection_item`  (
  `InspectionName` varchar(255) CHARACTER SET utf8 COLLATE utf8_croatian_ci NOT NULL,
  `medicalRecordsID` char(10) CHARACTER SET utf8 COLLATE utf8_croatian_ci NOT NULL,
  `paymentID` char(10) CHARACTER SET utf8 COLLATE utf8_croatian_ci NOT NULL,
  `picture` blob NULL,
  `result` text CHARACTER SET utf8 COLLATE utf8_croatian_ci NOT NULL,
  `analysis` text CHARACTER SET utf8 COLLATE utf8_croatian_ci NULL,
  PRIMARY KEY (`InspectionName`) USING BTREE,
  INDEX `InspectionRecordID`(`medicalRecordsID`) USING BTREE,
  INDEX `InspectionPaymentID`(`paymentID`) USING BTREE,
  CONSTRAINT `InspectionRecordID` FOREIGN KEY (`medicalRecordsID`) REFERENCES `medical_records` (`medicalRecordsID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `InspectionPaymentID` FOREIGN KEY (`paymentID`) REFERENCES `payment_slip` (`paymentID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_croatian_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for medical_records
-- ----------------------------
DROP TABLE IF EXISTS `medical_records`;
CREATE TABLE `medical_records`  (
  `medicalRecordsID` char(10) CHARACTER SET utf8 COLLATE utf8_croatian_ci NOT NULL,
  `patientID` char(10) CHARACTER SET utf8 COLLATE utf8_croatian_ci NOT NULL,
  `doctorID` char(10) CHARACTER SET utf8 COLLATE utf8_croatian_ci NOT NULL,
  `description` text CHARACTER SET utf8 COLLATE utf8_croatian_ci NULL,
  `office` varchar(255) CHARACTER SET utf8 COLLATE utf8_croatian_ci NOT NULL,
  `treatmentProgramme` text CHARACTER SET utf8 COLLATE utf8_croatian_ci NOT NULL,
  `Diagnoses` text CHARACTER SET utf8 COLLATE utf8_croatian_ci NOT NULL,
  `inspectionResult` text CHARACTER SET utf8 COLLATE utf8_croatian_ci NULL,
  PRIMARY KEY (`medicalRecordsID`) USING BTREE,
  INDEX `recordPatientID`(`patientID`) USING BTREE,
  INDEX `recodeDoctorID`(`doctorID`) USING BTREE,
  INDEX `recordOffice`(`office`) USING BTREE,
  CONSTRAINT `recodeDoctorID` FOREIGN KEY (`doctorID`) REFERENCES `doctor` (`doctorID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `recordOffice` FOREIGN KEY (`office`) REFERENCES `office` (`officeName`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `recordPatientID` FOREIGN KEY (`patientID`) REFERENCES `patient` (`patientID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_croatian_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for office
-- ----------------------------
DROP TABLE IF EXISTS `office`;
CREATE TABLE `office`  (
  `officeName` varchar(255) CHARACTER SET utf8 COLLATE utf8_croatian_ci NOT NULL,
  `headID` char(10) CHARACTER SET utf8 COLLATE utf8_croatian_ci NULL DEFAULT NULL,
  `number` int(11) NOT NULL,
  PRIMARY KEY (`officeName`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_croatian_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for patient
-- ----------------------------
DROP TABLE IF EXISTS `patient`;
CREATE TABLE `patient`  (
  `patientID` char(10) CHARACTER SET utf8 COLLATE utf8_croatian_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_croatian_ci NOT NULL,
  `sex` enum('男','女') CHARACTER SET utf8 COLLATE utf8_croatian_ci NOT NULL DEFAULT '男',
  `age` int(255) NOT NULL,
  `phoneNumber` char(11) CHARACTER SET utf8 COLLATE utf8_croatian_ci NOT NULL,
  `history` text CHARACTER SET utf8 COLLATE utf8_croatian_ci NULL COMMENT '既往病史',
  `address` varchar(255) CHARACTER SET utf8 COLLATE utf8_croatian_ci NULL DEFAULT NULL,
  `photo` blob NOT NULL COMMENT '证件照',
  PRIMARY KEY (`patientID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_croatian_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for payment_slip
-- ----------------------------
DROP TABLE IF EXISTS `payment_slip`;
CREATE TABLE `payment_slip`  (
  `paymentID` char(10) CHARACTER SET utf8 COLLATE utf8_croatian_ci NOT NULL,
  `patientID` char(10) CHARACTER SET utf8 COLLATE utf8_croatian_ci NOT NULL,
  `paymentItems` varchar(255) CHARACTER SET utf8 COLLATE utf8_croatian_ci NOT NULL,
  `amount` float(255, 2) NOT NULL,
  `time` datetime(0) NOT NULL,
  PRIMARY KEY (`paymentID`) USING BTREE,
  INDEX `paymentPatientID`(`patientID`) USING BTREE,
  CONSTRAINT `paymentPatientID` FOREIGN KEY (`patientID`) REFERENCES `patient` (`patientID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_croatian_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for prescription_list
-- ----------------------------
DROP TABLE IF EXISTS `prescription_list`;
CREATE TABLE `prescription_list`  (
  `prescriptionID` char(10) CHARACTER SET utf8 COLLATE utf8_croatian_ci NOT NULL,
  `patientID` char(10) CHARACTER SET utf8 COLLATE utf8_croatian_ci NOT NULL,
  `doctorID` char(10) CHARACTER SET utf8 COLLATE utf8_croatian_ci NOT NULL,
  `paymentID` char(10) CHARACTER SET utf8 COLLATE utf8_croatian_ci NOT NULL,
  `content` text CHARACTER SET utf8 COLLATE utf8_croatian_ci NOT NULL,
  PRIMARY KEY (`prescriptionID`) USING BTREE,
  INDEX `prescriptionPatientID`(`patientID`) USING BTREE,
  INDEX `prescriptionDoctorID`(`doctorID`) USING BTREE,
  INDEX `prescriptionPaymentID`(`paymentID`) USING BTREE,
  CONSTRAINT `prescriptionPatientID` FOREIGN KEY (`patientID`) REFERENCES `patient` (`patientID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `prescriptionDoctorID` FOREIGN KEY (`doctorID`) REFERENCES `doctor` (`doctorID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `prescriptionPaymentID` FOREIGN KEY (`paymentID`) REFERENCES `payment_slip` (`paymentID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_croatian_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for registration_slip
-- ----------------------------
DROP TABLE IF EXISTS `registration_slip`;
CREATE TABLE `registration_slip`  (
  `registrationID` char(10) CHARACTER SET utf8 COLLATE utf8_croatian_ci NOT NULL,
  `patientID` char(10) CHARACTER SET utf8 COLLATE utf8_croatian_ci NOT NULL,
  `doctorID` char(10) CHARACTER SET utf8 COLLATE utf8_croatian_ci NOT NULL,
  `office` varchar(255) CHARACTER SET utf8 COLLATE utf8_croatian_ci NOT NULL,
  `paymentID` char(10) CHARACTER SET utf8 COLLATE utf8_croatian_ci NOT NULL,
  `time` datetime(0) NOT NULL,
  `type` enum('专家门诊','特需号','会诊') CHARACTER SET utf8 COLLATE utf8_croatian_ci NOT NULL DEFAULT '专家门诊',
  PRIMARY KEY (`registrationID`) USING BTREE,
  INDEX `registrationPatinetID`(`patientID`) USING BTREE,
  INDEX `registrationDoctorID`(`doctorID`) USING BTREE,
  INDEX `registrationOffice`(`office`) USING BTREE,
  INDEX `registrationPaymentID`(`paymentID`) USING BTREE,
  CONSTRAINT `registrationDoctorID` FOREIGN KEY (`doctorID`) REFERENCES `doctor` (`doctorID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `registrationOffice` FOREIGN KEY (`office`) REFERENCES `office` (`officeName`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `registrationPatinetID` FOREIGN KEY (`patientID`) REFERENCES `patient` (`patientID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `registrationPaymentID` FOREIGN KEY (`paymentID`) REFERENCES `payment_slip` (`paymentID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_croatian_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- View structure for patientselectdoctor
-- ----------------------------
DROP VIEW IF EXISTS `patientselectdoctor`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `patientselectdoctor` AS select `doctor`.`doctorID` AS `doctorID`,`doctor`.`name` AS `name`,`doctor`.`sex` AS `sex`,`doctor`.`office` AS `office` from `doctor`;

-- ----------------------------
-- Triggers structure for table doctor
-- ----------------------------
DROP TRIGGER IF EXISTS `age_check_doctor`;
delimiter ;;
CREATE TRIGGER `age_check_doctor` BEFORE INSERT ON `doctor` FOR EACH ROW IF(NEW.age < 0 OR NEW.age > 150) THEN
		DELETE FROM doctor WHERE age = NEW.age;
END IF
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table doctor
-- ----------------------------
DROP TRIGGER IF EXISTS `phone_check_doctor`;
delimiter ;;
CREATE TRIGGER `phone_check_doctor` BEFORE INSERT ON `doctor` FOR EACH ROW IF((NEW.phoneNumber REGEXP '^1[0-9]{10}$') OR (NEW.phoneNumber REGEXP '^[0-9]{3,4}-[0-9]{7,8}')) = 0 THEN
	DELETE FROM doctor WHERE phoneNumber = NEW.phoneNumber;
END IF
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table office
-- ----------------------------
DROP TRIGGER IF EXISTS `number_check_office`;
delimiter ;;
CREATE TRIGGER `number_check_office` BEFORE INSERT ON `office` FOR EACH ROW IF(NEW.number <= 0) THEN
	DELETE FROM office WHERE number = NEW.number;
END IF
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table patient
-- ----------------------------
DROP TRIGGER IF EXISTS `age_check_patient`;
delimiter ;;
CREATE TRIGGER `age_check_patient` BEFORE INSERT ON `patient` FOR EACH ROW IF(NEW.age < 0 OR NEW.age > 150) THEN
		DELETE FROM patient WHERE age = NEW.age;
END IF
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table patient
-- ----------------------------
DROP TRIGGER IF EXISTS `phone_check_patient`;
delimiter ;;
CREATE TRIGGER `phone_check_patient` BEFORE INSERT ON `patient` FOR EACH ROW IF((NEW.phoneNumber REGEXP '^1[0-9]{10}$') OR (NEW.phoneNumber REGEXP '^[0-9]{3,4}-[0-9]{7,8}')) = 0 THEN
	DELETE FROM doctor WHERE phoneNumber = NEW.phoneNumber;
END IF
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
