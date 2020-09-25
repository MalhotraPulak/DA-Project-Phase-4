import subprocess as sp
import pymysql
import pymysql.cursors


def new_alpha_code(tablename, primarykey):
    QUERY = f'SELECT {primarykey} from {tablename}'

def option2():
    """
    Function to implement option 1
    """
    print("Not implemented")


def option3():
    """
    Function to implement option 2
    """
    print("Not implemented")


def option4():
    """
    Function to implement option 3
    """
    print("Not implemented")


def add_a_donor():
    print("first query godddam")
    # try:
    #     row = {}
    #     print("Enter new donor's details: ")
    #     name = (input("Name (Fname Minit Lname): ")).split(' ')
    #     row["Fname"] = name[0]
    #     row["Minit"] = name[1]
    #     row["Lname"] = name[2]
    #     row["Emplyoyee ID"] = input("Employee ID: ")
    #     row["Bdate"] = input("Birth Date (YYYY-MM-DD): ")
    #     row["Address"] = input("Address: ")
    #     row["Sex"] = input("Sex: ")
    #     row["Salary"] = float(input("Salary: "))
    #     row["Dno"] = int(input("Dno: "))
    #
    #
    #     print(query)
    #     cur.execute(query)
    #     con.commit()
    #
    #     print("Inserted Into Database")
    #
    # except Exception as e:
    #     con.rollback()
    #     print("Failed to insert into database")
    #     print(">>>>>>>>>>>>>", e)

    return


def dispatch(ch):
    if ch == 1:
        add_a_donor()
    elif ch == 2:
        option2()
    elif ch == 3:
        option3()
    elif ch == 4:
        option4()
    else:
        print("Error: Invalid Option")

username = "roott"
password = "pulak1234"
def ask_username_pass():
    # Can be skipped if you want to hard core username and password
    # username = input("Username: ")
    # password = input("Password: ")
    pass

def connect_to_database():
    global db, cursor
    sp.call('clear', shell=True)


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
        tmp = input("Enter Q to quit, any other key to continue")
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
        print("1. Get details of all donors")
        print("2. Generate a report on the current blood inventory")
        print("3. Option 3")
        print("4. Option 4")
        print("5. Logout")
        ch = int(input("Enter choice> "))
        tmp = sp.call('clear', shell=True)
        if ch == 5:
            break
        else:
            dispatch(ch)
            tmp = input("Enter any key to CONTINUE>")



db = None
connect_to_database()
if db is None:
    exit(1)
cursor = db.cursor()
loop()



