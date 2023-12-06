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

ALTER TABLE `employee`.`tluser` 
ADD COLUMN `role` VARCHAR(45) NULL AFTER `password`;

ALTER TABLE `employee`.`tluser` 
ADD COLUMN `status` VARCHAR(10) NULL AFTER `role`;
