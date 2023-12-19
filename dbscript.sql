create database employee;

CREATE TABLE `tluser` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(50) NULL,
  `last_name` VARCHAR(50) NULL,
  `contact_no` INT(10) NULL,
  `email_id` VARCHAR(50) NULL,
  `password` VARCHAR(1000) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_id_UNIQUE` (`email_id` ASC) VISIBLE,
  UNIQUE INDEX `contact_no_UNIQUE` (`contact_no` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

ALTER TABLE `tluser` 
CHANGE COLUMN `contact_no` `contact_no` VARCHAR(50) NULL DEFAULT NULL ;

ALTER TABLE `tluser` 
ADD COLUMN `role` VARCHAR(45) NULL AFTER `password`;

ALTER TABLE `tluser` 
ADD COLUMN `status` VARCHAR(10) NULL AFTER `role`;

CREATE TABLE `tb_manage_employee` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(50) NULL,
  `middle_name` VARCHAR(50) NULL,
  `last_name` VARCHAR(50) NULL,
  `contact` VARCHAR(20) NULL,
  `email_id` VARCHAR(50) NULL,
  `gender` VARCHAR(50) NULL,
  `city` VARCHAR(20) NULL,
  `Country` VARCHAR(20) NULL,
  ` Aadhar_number` INT(12) NULL,
  PRIMARY KEY (`id`))

ALTER TABLE `tb_manage_employee` 
CHANGE COLUMN ` Aadhar_number` ` Aadhar_number` VARCHAR(20) NULL DEFAULT NULL ;

ALTER TABLE `tb_manage_employee` 
CHANGE COLUMN ` Aadhar_number` `aadhar_number` VARCHAR(20) NULL DEFAULT NULL ;


CREATE TABLE `tb_metadata` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `element` VARCHAR(45) NULL,
  `type` VARCHAR(45) NULL,
  PRIMARY KEY (`id`));


ALTER TABLE `employee`.`tb_manage_employee` 
ADD COLUMN `birth_date` VARCHAR(45) NULL AFTER `aadhar_number`,
ADD COLUMN `blood_group` VARCHAR(45) NULL AFTER `birth_date`,
ADD COLUMN `pan_number` VARCHAR(20) NULL AFTER `blood_group`,
ADD COLUMN `total_experience` VARCHAR(45) NULL AFTER `pan_number`,
ADD COLUMN `designation` VARCHAR(45) NULL AFTER `total_experience`,
ADD COLUMN `employee_type` VARCHAR(45) NULL AFTER `designation`,
ADD COLUMN `joining_date` VARCHAR(45) NULL AFTER `employee_type`,
ADD COLUMN `current_address` VARCHAR(1000) NULL AFTER `joining_date`,
ADD COLUMN `permanent_address` VARCHAR(1000) NULL AFTER `current_address`;

CREATE TABLE `tb_attendance` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `employee_name` VARCHAR(45) NULL,
  `date` VARCHAR(45) NULL,
  `time` VARCHAR(45) NULL,
  `status` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))

ALTER TABLE `employee`.`tb_attendance` 
DROP COLUMN `status`,
DROP COLUMN `time`;

ALTER TABLE `employee`.`tb_attendance` 
CHANGE COLUMN `date` `date` DATETIME NULL DEFAULT NULL ;
