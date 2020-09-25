
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
  `donor_id` varchar(20) ,
  `employee_id` varchar(20) NOT NULL,
  `registration_id` varchar(20) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `middle_name` varchar(30),
  `last_name` varchar(30) NOT NULL,
  `phone_number` char(10) NOT NULL,
  `email_id` varchar(50) NOT NULL,
  `date_of_birth` date NOT NULL,
  `gender` varchar(20) NOT NULL,
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

