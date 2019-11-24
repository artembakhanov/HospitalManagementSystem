from os.path import dirname
from pathlib import Path

# WARNING! AUTO-GENERATED CONSTANTS! DO NOT CHANGE THEM!
PATH = Path(dirname(__file__))

# CONSTANTS
TABLE_USER = "GENERAL_USER"
TABLE_PATIENT = "PATIENT"
TABLE_WORKING_STAFF = "WORKING_STAFF"
TABLE_DOCTOR = "DOCTOR"
TABLE_NURSE = "NURSE"
TABLE_ACCOUNTANT = "ACCOUNTANT"
TABLE_PHARMACIST = "PHARMACIST"
TABLE_DOCTOR_TEAM = "DOCTOR_TEAM"
TABLE_NOTIFICATION = "NOTIFICATION"
TABLE_APPOINTMENT = "APPOINTMENT"
TABLE_INVOICE_BILL = "INVOICE_BILL"
TABLE_MEDICAL_RECORD = "MEDICAL_RECORD"
TABLE_PRESCRIPTION = "PRESCRIPTION"
TABLE_ADMIN = "ADMIN"
TABLE_BLOCKED = "BLOCKED"
TABLE_SCHEDULE = "SCHEDULE"
TABLE_STAFF_SCHEDULE = "STAFF_SCHEDULE"
VALUES_USER = "(Email, Fname, Lname, Mname, Gender, Birth_date, Address, Role, Password_hash)"
VALUES_PATIENT = "(User_id)"
VALUES_WORKING_STAFF = "(User_id, Salary, Qualification)"
VALUES_DOCTOR = "(W_staff_id, Room)"
VALUES_NURSE = "(W_staff_id, Doctor_team_id)"
VALUES_ACCOUNTANT = "(W_staff_id, License_id)"
VALUES_PHARMACIST = "(W_staff_id, Licence_id)"
VALUES_DOCTOR_TEAM = "(Doc_id)"
VALUES_NOTIFICATION = "(Notification_time, Title, Content, User_id)"
VALUES_APPOINTMENT = "(Room, Type, Start_time, End_time, Patient_id, Doctor_team_id, Invoice_bill_id)"
VALUES_INVOICE_BILL = "(Invoice_date, Price, Created_by, Is_paid)"
VALUES_MEDICAL_RECORD = "(Description, Med_rec_date, Appointment_id, Created_by)"
VALUES_PRESCRIPTION = ""
VALUES_ADMIN = ""
VALUES_BLOCKED = "(User_id, Admin_id)"
VALUES_SCHEDULE = "(Week_day, Start_time, End_time)"
VALUES_STAFF_SCHEDULE = "(W_staff_id, Schedule_id)"
ROLE_USER = 0
ROLE_PATIENT = 1
ROLE_WORKING_STAFF = 2
ROLE_NURSE = 4
ROLE_DOCTOR = 8
ROLE_ACCOUNTANT = 16
ROLE_PHARMACIST = 32
ROLE_CANTEEN_STAFF = 64
ROLE_ADMIN = 128
DATABASE_NAME = 'test10'
DATABASE_LOGIN = 'postgres'
DATABASE_PASSWORD = 'root1234'
DATABASE_SCHEMA_FILE = PATH / "SQL" / "init.sql"
QUERY1_FILE = PATH / "SQL" / "query1.sql"
QUERY2_FILE = PATH / "SQL" / "query2.sql"
QUERY3_FILE = PATH / "SQL" / "query3.sql"
QUERY4_FILE = PATH / "SQL" / "query4.sql"
QUERY5_FILE = PATH / "SQL" / "query5.sql"

with open(DATABASE_SCHEMA_FILE, encoding="utf-8") as f:
    CREATE_TABLES = f.read()

with open(QUERY1_FILE, encoding="utf-8") as f:
    QUERY1 = f.read()

with open(QUERY2_FILE, encoding="utf-8") as f:
    QUERY2 = f.read()

with open(QUERY3_FILE, encoding="utf-8") as f:
    QUERY3 = f.read()

with open(QUERY4_FILE, encoding="utf-8") as f:
    QUERY4 = f.read()

with open(QUERY5_FILE, encoding="utf-8") as f:
    QUERY5 = f.read()
