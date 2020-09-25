import subprocess as sp
import pymysql
import pymysql.cursors


def new_alpha_code(tablename, primarykey):
    sql = f'SELECT {primarykey} from {tablename}'
    cursor.execute(sql)
    results = cursor.fetchall()
    used = [0]
    print(used)
    for row in results:
        used.append(int(row[0]))
    return str(max(used) + 1)

def option2():
    """
    Function to implement option 1
    """
    print("Not implemented")

def add_a_donor():

    try:
        args = []
        fname = input("first name for donor: ")
        mname = input("middle name for donor: ")
        lname = input("last name for donor: ")
        eid = input("emp Id of Receptionist ")
        rid = input("regestriation id: ")
        phoneno = input("phone number: ")
        email = input("email id")
        dob = input("dob")
        gender = input("gender")
        date = input("date of registration")
        iid = new_alpha_code('donor', 'donor_id')
        sql = f'INSERT INTO donor (donor_id, employee_id, registration_id, first_name, middle_name, last_name, ' \
              f'phone_number, email_id, date_of_birth, gender, date_of_registration) VALUES ("{iid}", "{eid}", "{rid}",' \
              f' "{fname}", "{mname}", "{lname}", "{phoneno}", "{email}", "{dob}", "{gender}", "{date}");'
        print(sql)
        cursor.execute(sql)
        db.commit()
        print("Inserted into Database")
    except Exception as e:
        db.rollback()
        print("Failed to insert into database")
        print(">>>>>>>>>>>>>", e)

username = "root"
password = "pulak1234"


def ask_username_pass():
    # Can be skipped if you want to hard core username and password
    # username = input("Username: ")
    # password = input("Password: ")
    pass


def connect_to_database():
    global db, cursor
    sp.call('clear', shell=True)
    ask_username_pass()
    try:
        db = pymysql.connect(host='localhost',
                             user=username,
                             password=password,
                             db='BLOODBANK',
                             cursorclass=pymysql.cursors.DictCursor)
        sp.call('clear', shell=True)
    except:
        sp.call('clear', shell=True)
        print("Connection Refused: Either username or password is incorrect or user doesn't have access to database")
        tmp = input("Enter Q to quit, any other key to continue>")
        if tmp == 'Q':
            return
        connect_to_database()
    if db.open:
        print("Connected")
    else:
        print("Failed to connect")


def loop():
    while True:
        tmp = sp.call('clear', shell=True)
        # Here taking example of Employee Mini-world
        options = [
            "Add a Donor",
            "LUL"
        ]
        for i in range(0, len(options)):
            print(f'{i + 1}. {options[i]}')
        ch = 0
        try:
            ch = int(input("Enter choice> "))
        except ValueError:
            print("Error: Integer Dumbass")
            continue
        sp.call('clear', shell=True)
        if ch == 5:
            break
        else:
            if ch == 1:
                add_a_donor()
            elif ch == 2:
                option2()
            elif ch == 3:
                pass
            elif ch == 4:
                pass
            else:
                print("Error: Invalid Option")
            input("Enter any key to CONTINUE>")


db = None
connect_to_database()
if db is None:
    exit(1)
cursor = db.cursor()
loop()
