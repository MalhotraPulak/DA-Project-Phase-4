import subprocess as sp
import pymysql
import pymysql.cursors
from prettytable import from_db_cursor
from datetime import date

username = ""
password = ""  ## ashwin


def connectToDatabase():
    global db, cursor
    sp.call('clear', shell=True)

    try:
        username = input("Username: ")
        password = input("Password: ")
        db = pymysql.connect(host='localhost',
                             user=username,
                             password=password,
                             db='bloodbank')
        sp.call('clear', shell=True)
        if db.open:
            print("Connected")
        else:
            print("Failed to connect")
    except Exception:
        sp.call('clear', shell=True)
        print("Connection Refused: Either username or password is incorrect or user doesn't have access to database")
        tmp = input("Enter Q to quit, any other key to continue>")
        if tmp == 'Q':
            return
        connectToDatabase()

# ------------------------ INSERTION QUERIES ------------------------
def addDonor():
    try:
        donor = {}
        donor["fname"] = input("First name: ")
        donor["mname"] = input("Middle name: ")
        donor["lname"] = input("Last name: ")

        donor["dob"] = input("Date of Birth (YYYY/MM/DD): ")
        year, month, day = map(int, donor["dob"].split("/"))
        if ((date.today() - date(year, month, day)).days // 365) < 18:
            print("Donor must be 18 years or above to donate!")
            return

        donor["eid"] = int(input("Employee ID of Receptionist: "))
        donor["phoneno"] = input("Phone Number: ")
        donor["email"] = input("Email ID: ")
        donor["sex"] = input("Sex (M/F) : ")

        SQL_query = "INSERT INTO donor (employee_id, first_name, middle_name, last_name, phone_number, email_id, date_of_birth, gender, date_of_registration) " \
                    "VALUES({}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', CURDATE())".format(
                        donor["eid"], donor["fname"], donor["mname"], donor["lname"], donor["phoneno"], donor["email"], donor["dob"], donor["sex"]
                    )

        print(SQL_query)
        cursor.execute(SQL_query)
        db.commit()
        print("Insert successful")

    except Exception as e:
        db.rollback()
        print("Failed to insert into database")
        print("Error >>>>>>>>>>>>>", e)


def addReceptionist():
    try:
        receptionist = {}
        receptionist["fname"] = input("First name: ")
        receptionist["mname"] = input("Middle name: ")
        receptionist["lname"] = input("Last name: ")
        receptionist["cid"] = int(input("Centre ID:  "))
        receptionist["phoneno"] = input("Phone Number: ")

        SQL_query = "INSERT INTO receptionist (center_id, first_name, middle_name, last_name, phone_number) " \
                    "VALUES({}, '{}', '{}', '{}', '{}')".format(
                        receptionist["cid"], receptionist["fname"], receptionist["mname"], receptionist["lname"], receptionist["phoneno"]
                    )

        print(SQL_query)
        cursor.execute(SQL_query)
        db.commit()
        print("Insert successful")

    except Exception as e:
        db.rollback()
        print("Failed to insert into database")
        print("Error >>>>>>>>>>>>>", e)


def addBloodDonationCenter():
    try:
        center = {}
        center["address"] = input("Address: ")
        center["phoneno"] = input("Phone Number: ")

        SQL_query = "INSERT INTO blood_donation_center (phone_number, address) " \
                    "VALUES('{}', '{}')".format(center["phoneno"], center["address"])

        print(SQL_query)
        cursor.execute(SQL_query)
        db.commit()
        print("Successfully inserted into Database")

    except Exception as e:
        db.rollback()
        print("Insert successful")
        print("Error >>>>>>>>>>>>>", e)


# def addDonation():
#     pass
#
#
# def addBlood():
#     pass
#
#
# def addTestResult():
#     pass
#
#
# def addToInventory():
#     try:
#         inventory = {}
#         inventory["bldbarcode"] = int(input("Blood Barcode: "))
#         inventory["compid"] = int(input("Component ID: "))
#         inventory["dateofstorage"] = input("Date of Storage: ")
#
#         SQL_query = "INSERT INTO blood_inventory (blood_barcode, component_id, date_of_storage)" \
#                     "VALUES ({}, {}, '{}')".format(inventory["bldbarcode"], inventory["compid"], inventory["dateofstorage"])
#
#         print(SQL_query)
#         cursor.execute(SQL_query)
#         db.commit()
#         print("Insert successful")
#
#     except Exception as e:
#         db.rollback()
#         print("Failed to insert into database")
#         print("Error >>>>>>>>>>>>>", e)


# ------------------------ UPDATE QUERIES ------------------------
def updateDonorDetails():
    try:
        donor_id = int(input("Donor ID: "))
        options = [
            "Update Phone Number",
            "Update Email ID",
            "Add New Address",
            "Remove Address"
        ]
        for i in range(0, len(options)):
            print(f'{i + 1}. {options[i]}')
        try:
            choice = int(input("Enter choice> "))
        except ValueError:
            print("Error: Invalid Choice")
            return

        if choice == 1:
            phone_number = input("New Phone Number: ")
            SQL_query = "UPDATE donor SET phone_number = '{}' WHERE donor_id = {}".format(phone_number, donor_id)
        elif choice == 2:
            email_id = input("New Email ID: ")
            SQL_query = "UPDATE donor SET email_id = '{}' WHERE donor_id = {}".format(email_id, donor_id)
        elif choice == 3:
            address = input("New Address: ")
            SQL_query = "INSERT INTO donor_address (donor_id, address) " \
                        "VALUES ({}, '{}')".format(donor_id, address)
        elif choice == 4:
            address = input("Address: ")
            SQL_query = "DELETE FROM donor_address WHERE donor_id = {} AND address = '{}'".format(donor_id, address)
        else:
            return

        print(SQL_query)
        cursor.execute(SQL_query)
        db.commit()
        print("Update Successful")

    except Exception as e:
        db.rollback()
        print("Failed to update database")
        print("Error >>>>>>>>>>>>>", e)


# ------------------------ DELETION QUERIES ------------------------
def removeDonor():
    try:
        donor_id = int(input("Donor ID: "))
        SQL_query = "DELETE FROM donor WHERE donor_id = {}".format(donor_id)

        print(SQL_query)
        cursor.execute(SQL_query)
        db.commit()
        print("Delete successful")

    except Exception as e:
        db.rollback()
        print("Failed to delete from database")
        print("Error >>>>>>>>>>>>>", e)


def removeOrderedSamplesFromInventory():
    try:
        SQL_query = "DELETE FROM blood_inventory WHERE order_id IS NOT NULL"

        print(SQL_query)
        cursor.execute(SQL_query)
        db.commit()
        print("Delete successful")

    except Exception as e:
        db.rollback()
        print("Failed to delete from database")
        print("Error >>>>>>>>>>>>>", e)


def removeExpiredSamplesFromInventory():
    try:
        SQL_query = "DELETE blood_inventory FROM blood_inventory " \
                    "JOIN component ON blood_inventory.component_id = component.component_id " \
                    "WHERE order_id IS NULL AND date_of_storage + INTERVAL max_storage_duration DAY < CURDATE()"

        print(SQL_query)
        cursor.execute(SQL_query)
        db.commit()
        print("Delete successful")

    except Exception as e:
        db.rollback()
        print("Failed to delete from database")
        print("Error >>>>>>>>>>>>>", e)


# ------------------------ SELECTION QUERIES ------------------------
def getDonorDetails():
    try:
        SQL_query = "SELECT DISTINCT donor.donor_id, first_name, middle_name, last_name, phone_number, email_id, date_of_birth, gender, blood_type FROM donor " \
                    "JOIN donor_participation ON donor.donor_id = donor_participation.donor_id " \
                    "JOIN blood ON donor_participation.blood_barcode = blood.blood_barcode"

        cursor.execute(SQL_query)
        table = from_db_cursor(cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print("Query failed")
        print("Error >>>>>>>>>>>>>", e)


def generateBloodInventoryReport():
    try:
        SQL_query = "SELECT * FROM blood_inventory ORDER BY date_of_storage"

        cursor.execute(SQL_query)
        table = from_db_cursor(cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print("Query failed")
        print("Error >>>>>>>>>>>>>", e)


def getDailyOrders():
    try:
        date = input("Date (YYYY/MM/DD): ")
        SQL_query = "SELECT * FROM orders WHERE date_of_order = '{}'".format(date)

        cursor.execute(SQL_query)
        table = from_db_cursor(cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print("Query failed")
        print("Error >>>>>>>>>>>>>", e)


def getDonorsByAge():
    try:
        lower_age, upper_age = map(int, input("Lower and Upper Ages: ").split())
        SQL_query = "SELECT * FROM donor WHERE TIMESTAMPDIFF(year, date_of_birth, CURDATE()) BETWEEN {} AND {}".format(lower_age, upper_age)

        cursor.execute(SQL_query)
        table = from_db_cursor(cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print("Query failed")
        print("Error >>>>>>>>>>>>>", e)


def findCommonlyOrderedBloodTypes():
    try:
        SQL_query = "SELECT blood_type, component_type, COUNT(*) AS total_orders FROM blood_inventory " \
                    "JOIN blood ON blood_inventory.blood_barcode = blood.blood_barcode " \
                    "JOIN component ON blood_inventory.component_id = component.component_id " \
                    "WHERE order_id IS NOT NULL " \
                    "GROUP BY blood_type, component_type " \
                    "ORDER BY total_orders DESC"

        cursor.execute(SQL_query)
        table = from_db_cursor(cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print("Query failed")
        print("Error >>>>>>>>>>>>>", e)


def findTotalStock():
    try:
        SQL_query = "SELECT blood_type, component_type, COUNT(*) AS total_stock FROM blood_inventory " \
                    "JOIN blood ON blood_inventory.blood_barcode = blood.blood_barcode " \
                    "JOIN component ON blood_inventory.component_id = component.component_id " \
                    "WHERE order_id IS NULL " \
                    "GROUP BY blood_type, component_type " \
                    "ORDER BY total_stock DESC"

        cursor.execute(SQL_query)
        table = from_db_cursor(cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print("Query failed")
        print("Error >>>>>>>>>>>>>", e)


def getDonorsFromArea():
    try:
        search_string = input("Search String: ")
        SQL_query = "SELECT donor.*, donor_address.address FROM donor " \
                    "JOIN donor_address ON donor.donor_id = donor_address.donor_id " \
                    "WHERE donor_address.address LIKE CONCAT('%', '{}', '%')".format(search_string)

        cursor.execute(SQL_query)
        table = from_db_cursor(cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print("Query failed")
        print("Error >>>>>>>>>>>>>", e)


def getDonorsFromBloodType():
    try:
        blood_type = input("Blood Type: " )
        SQL_query = "SELECT DISTINCT donor.* FROM donor " \
                    "JOIN donor_participation ON donor.donor_id = donor_participation.donor_id " \
                    "JOIN blood ON donor_participation.blood_barcode = blood.blood_barcode " \
                    "WHERE blood_type = '{}'".format(blood_type)

        cursor.execute(SQL_query)
        table = from_db_cursor(cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print("Query failed")
        print("Error >>>>>>>>>>>>>", e)


def getDonorsFromTestResults():
    try:
        SQL_query = "SELECT DISTINCT donor.* FROM donor " \
                    "JOIN donor_participation ON donor.donor_id = donor_participation.donor_id " \
                    "JOIN blood ON donor_participation.blood_barcode = blood.blood_barcode " \
                    "JOIN test_result ON blood.blood_barcode = test_result.blood_barcode " \
                    "WHERE " \
                        "test_result.hiv1 + test_result.hiv2 + " \
                        "test_result.hepatitis_b + test_result.hepatitis_c + " \
                        "test_result.htlv1 + test_result.htlv2 + " \
                        "test_result.syphilis = 0"

        cursor.execute(SQL_query)
        table = from_db_cursor(cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print("Query failed")
        print("Error >>>>>>>>>>>>>", e)


def getDonorsFromEmployee():
    try:
        employee_id = int(input("Employee ID: "))
        SQL_query = "SELECT * FROM donor WHERE employee_id = {}".format(employee_id)

        cursor.execute(SQL_query)
        table = from_db_cursor(cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print("Query failed")
        print("Error >>>>>>>>>>>>>", e)


def getDonorsRegisteredAtCenter():
    try:
        center_id = int(input("Center ID: "))
        SQL_query = "SELECT donor.* FROM donor " \
                    "JOIN receptionist ON donor.employee_id = receptionist.employee_id " \
                    "JOIN blood_donation_center ON receptionist.center_id = blood_donation_center.center_id " \
                    "WHERE blood_donation_center.center_id = {}".format(center_id)

        cursor.execute(SQL_query)
        table = from_db_cursor(cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print("Query failed")
        print("Error >>>>>>>>>>>>>", e)


def getDonorsDonatedAtCenter():
    try:
        center_id = int(input("Center ID: "))
        SQL_query = "SELECT DISTINCT donor.* FROM donor " \
                    "JOIN donor_participation ON donor.donor_id = donor_participation.donor_id " \
                    "JOIN blood_donation_center ON donor_participation.center_id = blood_donation_center.center_id " \
                    "WHERE blood_donation_center.center_id = {}".format(center_id)

        cursor.execute(SQL_query)
        table = from_db_cursor(cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print("Query failed")
        print("Error >>>>>>>>>>>>>", e)


def findExpiredBlood():
    try:
        SQL_query = "SELECT blood_inventory.blood_barcode, blood_inventory.component_id, blood_inventory.date_of_storage, component.max_storage_duration FROM blood_inventory " \
                    "JOIN component ON blood_inventory.component_id = component.component_id " \
                    "WHERE order_id IS NULL AND date_of_storage + INTERVAL max_storage_duration DAY < CURDATE()"

        cursor.execute(SQL_query)
        table = from_db_cursor(cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print("Query failed")
        print("Error >>>>>>>>>>>>>", e)


# ------------------------ COMMAND LINE INTERFACE ------------------------
def loop():
    while True:
        sp.call('clear', shell=True)
        options = [
            "Add a Donor",
            "Add a Receptionist",
            "Add a Blood Donation Center",
            "Get Details of all Donors who have Donated",
            "Generate Blood Inventory Report",
            "Get Orders on a Particular Date",
            "Find Most Commonly Ordered Blood Type and Component Type",
            "Find Total Stock of Each Blood Type and Component Type",
            "Find Samples in Blood Inventory which have Expired",
            "Get Donors in a Specific Age Group",
            "Get Donors living in a Particular Area",
            "Get Donors with a Specific Blood Type",
            "Get Donors with All Test Results Negative",
            "Get Donors Registered by a Particular Employee",
            "Get Donors Registered at a Particular Center",
            "Get Donors who have Donated at a Particular Center",
            "Update Details of a Donor",
            "Remove a Donor",
            "Delete Samples from Inventory (which have been ordered)",
            "Delete Samples from Inventory (which have expired)",
            "Quit"
        ]

        for i in range(0, len(options)):
            print(f'{i + 1}. {options[i]}')
        try:
            choice = int(input("Enter choice> "))
        except ValueError:
            print("Error: Invalid Choice")
            continue

        sp.call('clear', shell=True)

        if choice == 21:
            break
        else:
            if choice == 1:
                addDonor()
            elif choice == 2:
                addReceptionist()
            elif choice == 3:
                addBloodDonationCenter()
            elif choice == 4:
                getDonorDetails()
            elif choice == 5:
                generateBloodInventoryReport()
            elif choice == 6:
                getDailyOrders()
            elif choice == 7:
                findCommonlyOrderedBloodTypes()
            elif choice == 8:
                findTotalStock()
            elif choice == 9:
                findExpiredBlood()
            elif choice == 10:
                getDonorsByAge()
            elif choice == 11:
                getDonorsFromArea()
            elif choice == 12:
                getDonorsFromBloodType()
            elif choice == 13:
                getDonorsFromTestResults()
            elif choice == 14:
                getDonorsFromEmployee()
            elif choice == 15:
                getDonorsRegisteredAtCenter()
            elif choice == 16:
                getDonorsDonatedAtCenter()
            elif choice == 17:
                updateDonorDetails()
            elif choice == 18:
                removeDonor()
            elif choice == 19:
                removeOrderedSamplesFromInventory()
            elif choice == 20:
                removeExpiredSamplesFromInventory()
            else:
                print("Error: Invalid Choice")
            input("Enter any key to CONTINUE> ")


db = None
cursor = None
#db = pymysql.connections.Connection(user=username, password=password)
connectToDatabase()
if db is None:
    exit(1)
else:
    cursor = db.cursor()
    loop()
