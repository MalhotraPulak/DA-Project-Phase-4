DROP DATABASE IF EXISTS `BLOODBANK`;
CREATE SCHEMA `BLOODBANK`;
USE `BLOODBANK`;

CREATE TABLE `blood_donation_center` (
  `center_id` varchar(20),
  `phone_number` char(10) NOT NULL,
  `address` varchar(100) NOT NULL,
  PRIMARY KEY (`center_id`)
);

CREATE TABLE `receptionist` (
  `employee_id` varchar(20),
  `center_id` varchar(20) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `middle_name` varchar(30),
  `last_name` varchar(30) NOT NULL,
  `phone_number` char(10) NOT NULL,
  PRIMARY KEY (`employee_id`),
  FOREIGN KEY (`center_id`) REFERENCES `blood_donation_center` (`center_id`)
);

CREATE TABLE `donor` (
  `donor_id` varchar(20),
  `employee_id` varchar(20) NOT NULL,
  `registration_id` varchar(20) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `middle_name` varchar(30),
  `last_name` varchar(30) NOT NULL,
  `phone_number` char(10) NOT NULL,
  `email_id` varchar(50) NOT NULL,
  `date_of_birth` date NOT NULL,
  `gender` char(1) NOT NULL,
  `date_of_registration` date NOT NULL,
  PRIMARY KEY (`donor_id`),
  FOREIGN KEY (`employee_id`) REFERENCES `receptionist` (`employee_id`)
);

CREATE TABLE `donor_address` (
  `donor_id` varchar(20),
  `address` varchar(100),
  PRIMARY KEY (`donor_id`, `address`),
  FOREIGN KEY (`donor_id`) REFERENCES `donor` (`donor_id`)
);

CREATE TABLE `donation` (
  `donation_id` varchar(20),
  `blood_pressure` varchar(10) NOT NULL,
  `haemoglobin_level` varchar(10) NOT NULL,
  `date_of_donation` date NOT NULL,
  `weight` decimal NOT NULL,
  `travel_history` varchar(255) NOT NULL,
  PRIMARY KEY (`donation_id`)
);

CREATE TABLE `blood_cost` (
  `blood_type` varchar(20),
  `blood_type_cost` decimal NOT NULL,
  PRIMARY KEY (`blood_type`)
);

CREATE TABLE `blood` (
  `blood_barcode` varchar(20),
  `blood_type` varchar(20) NOT NULL,
  `description` varchar(255),
  PRIMARY KEY (`blood_barcode`),
  FOREIGN KEY (`blood_type`) REFERENCES `blood_cost` (`blood_type`)
);

CREATE TABLE `donor_participation` (
  `blood_barcode` varchar(20),
  `donor_id` varchar(20) NOT NULL,
  `center_id` varchar(20) NOT NULL,
  `donation_id` varchar(20) NOT NULL,
  PRIMARY KEY (`blood_barcode`),
  FOREIGN KEY (`blood_barcode`) REFERENCES `blood` (`blood_barcode`),
  FOREIGN KEY (`donor_id`) REFERENCES `donor` (`donor_id`),
  FOREIGN KEY (`center_id`) REFERENCES `blood_donation_center` (`center_id`),
  FOREIGN KEY (`donation_id`) REFERENCES `donation` (`donation_id`)
);

CREATE TABLE `test_result` (
  `blood_barcode` varchar(20),
  `hiv1` bool NOT NULL,
  `hiv2` bool NOT NULL,
  `hepatitis_b` bool NOT NULL,
  `hepatitis_c` bool NOT NULL,
  `htlv1` bool NOT NULL,
  `htlv2` bool NOT NULL,
  `syphilis` bool NOT NULL,
  PRIMARY KEY (`blood_barcode`),
  FOREIGN KEY (`blood_barcode`) REFERENCES `blood` (`blood_barcode`)
);

CREATE TABLE `component` (
  `component_id` varchar(20),
  `component_type` varchar(20) NOT NULL,
  `standard_quantity` decimal NOT NULL,
  `storage_temperature` decimal NOT NULL,
  `max_storage_duration` int NOT NULL,
  PRIMARY KEY (`component_id`)
);

CREATE TABLE `hospital` (
  `hospital_id` varchar(20),
  `name` varchar(30) NOT NULL,
  `address` varchar(100) NOT NULL,
  `email_id` varchar(50) NOT NULL,
  `phone_number` char(10) NOT NULL,
  PRIMARY KEY (`hospital_id`)
);

CREATE TABLE `orders` (
  `order_id` varchar(20),
  `hospital_id` varchar(20) NOT NULL,
  `date_of_order` date NOT NULL,
  `total_cost` decimal NOT NULL,
  PRIMARY KEY (`order_id`),
  FOREIGN KEY (`hospital_id`) REFERENCES `hospital` (`hospital_id`)
);

CREATE TABLE `order_components` (
  `order_id` varchar(20),
  `blood_type` varchar(20),
  `component_type` varchar(20),
  `quantity` int NOT NULL,
  PRIMARY KEY (`order_id`, `blood_type`, `component_type`),
  FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`)
);

CREATE TABLE `blood_inventory` (
  `blood_barcode` varchar(20),
  `component_id` varchar(20),
  `order_id` varchar(20),
  `date_of_storage` date NOT NULL,
  PRIMARY KEY (`blood_barcode`, `component_id`),
  FOREIGN KEY (`blood_barcode`) REFERENCES `blood` (`blood_barcode`),
  FOREIGN KEY (`component_id`) REFERENCES `component` (`component_id`),
  FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`)
);


# QUERYING THE DATABASE

# SELECTTION QUERIES
SELECT donor.donor_id, registration_id, first_name, middle_name, last_name, phone_number, email_id, date_of_birth, gender, blood_type FROM donor 
    JOIN donor_participation ON donor.donor_id = donor_participation.donor_id
    JOIN blood ON donor_participation.blood_barcode = blood.blood_barcode;

SELECT * FROM blood_inventory ORDER BY date_of_storage;


# PROJECTION QUERIES
SELECT * FROM orders WHERE date_of_order = CURDATE();

SELECT donor_id FROM donor WHERE TIMESTAMPDIFF(year, date_of_birth, CURDATE()) BETWEEN 20 AND 30;


# AGGREGATE FUNCTIONS
SELECT blood_type, component_type, COUNT(*) AS total_orders FROM blood_inventory
    JOIN blood ON blood_inventory.blood_barcode = blood.blood_barcode
    JOIN component ON blood_inventory.component_id = component.component_id
WHERE order_id IS NOT NULL
GROUP BY blood_type, component_type
ORDER BY total_orders DESC;

SELECT blood_type, component_type, COUNT(*) AS total_orders FROM blood_inventory
    JOIN blood ON blood_inventory.blood_barcode = blood.blood_barcode
    JOIN component ON blood_inventory.component_id = component.component_id
WHERE order_id IS NULL
GROUP BY blood_type, component_type;


# SEARCH FUNCTIONS
SELECT donor.* FROM donor 
    JOIN donor_address ON donor.donor_id = donor_address.donor_id
WHERE donor_address.address LIKE "%bangalore%";


# ANALYSIS QUERIES
SELECT donor.* FROM donor 
    JOIN donor_participation ON donor.donor_id = donor_participation.donor_id
    JOIN blood ON donor_participation.blood_barcode = blood.blood_barcode
WHERE blood_type = "B+";

SELECT donor.* FROM donor 
    JOIN donor_participation ON donor.donor_id = donor_participation.donor_id
    JOIN blood ON donor_participation.blood_barcode = blood.blood_barcode
    JOIN test_result ON blood.blood_barcode = test_result.blood_barcode
WHERE 
    test_result.hiv1 + test_result.hiv2 + 
    test_result.hepatitis_b + test_result.hepatitis_c + 
    test_result.htlv1 + test_result.htlv2 + 
    test_result.syphilis = 0; 

SELECT * FROM donor WHERE employee_id = "John Doe";

SELECT donor.* FROM donor 
    JOIN donor_participation ON donor.donor_id = donor_participation.donor_id
    JOIN blood_donation_center ON donor_participation.center_id = blood_donation_center.center_id
WHERE blood_donation_center.center_id = "A112BC";

SELECT blood_inventory.blood_barcode, blood_inventory.component_id, blood_inventory.date_of_storage FROM blood_inventory
    JOIN component ON blood_inventory.component_id = component.component_id
WHERE order_id IS NULL AND date_of_storage + INTERVAL max_storage_duration DAY < CURDATE();


# INSERTION QUERIES
INSERT INTO donor ZZ(donor_id, employee_id, registration_id, first_name, middle_name, last_name, phone_number, email_id, date_of_birth, gender, date_of_registration)
VALUES (
    "1", "123", "55", "John", NULL, "Doe", "9980221156", "johndoe@yoyo.com", "1995/06/12", "M", CURDATE()
);

INSERT INTO blood (blood_barcode, blood_type, description) 
VALUES (
    "11423", "B+", "B positive blood"
); 

INSERT INTO blood_inventory (blood_barcode, component_id, date_of_storage) 
VALUES (
    "11423", "3", "2020/08/06"
);


# UPDATE QUERIES
UPDATE donor SET phone_number = "8890096331" WHERE donor_id = "1";
UPDATE donor SET email_id = "johndoe&gmail.com" WHERE donor_id = "1";

INSERT INTO donor_address (donor_id, address) VALUES ("1", "South India");
DELETE FROM donor_address WHERE donor_id = "1" AND address = "North India";


# DELETE QUERIES
DELETE FROM donor WHERE donor_id = "1";

DELETE FROM blood_inventory WHERE order_id IS NOT NULL;

DELETE blood_inventory FROM blood_inventory
    JOIN component ON blood_inventory.component_id = component.component_id
WHERE order_id IS NULL AND date_of_storage + INTERVAL max_storage_duration DAY < CURDATE();


