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

ALTER TABLE `employee`.`tb_manage_employee` 
CHANGE COLUMN ` Aadhar_number` ` Aadhar_number` VARCHAR(20) NULL DEFAULT NULL ;

ALTER TABLE `employee`.`tb_manage_employee` 
CHANGE COLUMN ` Aadhar_number` `aadhar_number` VARCHAR(20) NULL DEFAULT NULL ;
