# QUERYING THE DATABASE

# SELECTTION QUERIES
SELECT DISTINCT donor.donor_id, first_name, middle_name, last_name, phone_number, email_id, date_of_birth, gender, blood_type FROM donor 
    JOIN donor_participation ON donor.donor_id = donor_participation.donor_id
    JOIN blood ON donor_participation.blood_barcode = blood.blood_barcode;

SELECT * FROM blood_inventory ORDER BY date_of_storage;


# PROJECTION QUERIES
SELECT * FROM orders WHERE date_of_order = "2020/12/1";

SELECT * FROM donor WHERE TIMESTAMPDIFF(year, date_of_birth, CURDATE()) BETWEEN 20 AND 30;


# AGGREGATE FUNCTIONS
SELECT blood_type, component_type, COUNT(*) AS total_orders FROM blood_inventory
    JOIN blood ON blood_inventory.blood_barcode = blood.blood_barcode
    JOIN component ON blood_inventory.component_id = component.component_id
WHERE order_id IS NOT NULL
GROUP BY blood_type, component_type
ORDER BY total_orders DESC;

SELECT blood_type, component_type, COUNT(*) AS total_stock FROM blood_inventory
    JOIN blood ON blood_inventory.blood_barcode = blood.blood_barcode
    JOIN component ON blood_inventory.component_id = component.component_id
WHERE order_id IS NULL
GROUP BY blood_type, component_type
ORDER BY total_stock DESC;


# SEARCH FUNCTIONS
SELECT donor.*, donor_address.address FROM donor 
    JOIN donor_address ON donor.donor_id = donor_address.donor_id
WHERE donor_address.address LIKE CONCAT('%', 'bangalore', '%');


# ANALYSIS QUERIES
SELECT DISTINCT donor.* FROM donor 
    JOIN donor_participation ON donor.donor_id = donor_participation.donor_id
    JOIN blood ON donor_participation.blood_barcode = blood.blood_barcode
WHERE blood_type = 'B+';

SELECT DISTINCT donor.* FROM donor 
    JOIN donor_participation ON donor.donor_id = donor_participation.donor_id
    JOIN blood ON donor_participation.blood_barcode = blood.blood_barcode
    JOIN test_result ON blood.blood_barcode = test_result.blood_barcode
WHERE 
    test_result.hiv1 + test_result.hiv2 + 
    test_result.hepatitis_b + test_result.hepatitis_c + 
    test_result.htlv1 + test_result.htlv2 + 
    test_result.syphilis = 0;

SELECT * FROM donor WHERE employee_id = 12;

# find all donors registered at a particular center
SELECT donor.* FROM donor 
    JOIN receptionist ON donor.employee_id = receptionist.employee_id
    JOIN blood_donation_center ON receptionist.center_id = blood_donation_center.center_id
WHERE blood_donation_center.center_id = 12;

# find all donors who have donated at a particular center
SELECT DISTINCT donor.* FROM donor 
    LEFT JOIN donor_participation ON donor.donor_id = donor_participation.donor_id
    LEFT JOIN blood_donation_center ON donor_participation.center_id = blood_donation_center.center_id
WHERE blood_donation_center.center_id = 12;

SELECT blood_inventory.blood_barcode, blood_inventory.component_id, blood_inventory.date_of_storage, component.max_storage_duration FROM blood_inventory
    JOIN component ON blood_inventory.component_id = component.component_id
WHERE order_id IS NULL AND date_of_storage + INTERVAL max_storage_duration DAY < CURDATE();


# INSERTION QUERIES
INSERT INTO donor (employee_id, first_name, middle_name, last_name, phone_number, email_id, date_of_birth, gender, date_of_registration) 
VALUES (
    1, "John", "", "Doe", "9980221156", "johndoe@yoyo.com", "1995/06/12", "M", CURDATE()
);

INSERT INTO blood (blood_type, description) 
VALUES (
    "B+", "B positive blood"
);

INSERT INTO blood_inventory (blood_barcode, component_id, date_of_storage) 
VALUES (
    114, 3, "2020/08/06"
);


# UPDATE QUERIES
UPDATE donor SET phone_number = "8890096331" WHERE donor_id = 1;
UPDATE donor SET email_id = "johndoe&gmail.com" WHERE donor_id = 1;

INSERT INTO donor_address (donor_id, address) VALUES (1, "South India");
DELETE FROM donor_address WHERE donor_id = 1 AND address = "North India";


# DELETE QUERIES
DELETE FROM donor WHERE donor_id = 1;

DELETE FROM blood_inventory WHERE order_id IS NOT NULL;

DELETE blood_inventory FROM blood_inventory
    JOIN component ON blood_inventory.component_id = component.component_id
WHERE order_id IS NULL AND date_of_storage + INTERVAL max_storage_duration DAY < CURDATE();