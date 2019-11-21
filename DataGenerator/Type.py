import datetime
import random

from DataGenerator.DateGenerator import gen_datetime
from DataGenerator.Pool import GeneralPool, AppointmentIDPool
from DataGenerator.config import DOCTOR_NUMBER, APPOINTMENT_NOTIFICATION_TITLE, APPOINTMENT_NOTIFICATION_CONTENT, \
    ACCOUNTANT_NUMBER
from static import *

MIDDLE_NAME_CHANCE = 0.5


class User:
    def __init__(self):
        self.user_id = None
        self.fname = None
        self.lname = None
        self.mname = ""
        self.email = None
        self.password_hash = None
        self.birth_date = None
        self.gender = None
        self.address = None
        self.role = None

    def __str__(self):
        return f"User {{" \
               f"user_id={self.user_id}" \
               f"fname={self.fname} " \
               f"lname={self.lname} " \
               f"mname={self.mname} " \
               f"email={self.email} " \
               f"password_hash={self.password_hash} " \
               f"birth_date={self.birth_date} " \
               f"gender={self.gender} " \
               f"address={self.address}" \
               f"}}"

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def generate(n):
        pool = GeneralPool()
        users = []
        for i in range(n):
            user = User()
            user.user_id = i + 1
            user.email = pool.get("email")
            user.fname = pool.get("fname").capitalize()  # todo: capitalize it
            user.lname = pool.get("lname").capitalize()
            user.address = pool.get("address")
            user.password_hash = pool.get("password")
            if random.random() >= MIDDLE_NAME_CHANCE:
                user.mname = pool.get("fname").capitalize()
            user.gender = "M" if random.random() >= 0.5 else "F"
            user.birth_date = None  # TODO: make birthdate generator
            users.append(user)

        return users

    def specialize(self, cls, **kwargs):
        self.__class__ = cls
        for key, value in kwargs.items():
            self.__setattr__(key, value)

    def sql(self):
        return f"INSERT INTO {TABLE_USER} " \
               f"VALUES ('{self.email}', " \
               f"'{self.fname}', '{self.lname}', " \
               f"'{self.mname}', '{self.gender}', " \
               f"{self.birth_date} '{self.address}', " \
               f"{self.role}, '{self.password_hash}'," \
               f"NULL);\n"


class Patient(User):
    def __init__(self):
        super(Patient, self).__init__()
        self.patient_id = None

    @staticmethod
    def generate(n):
        users = super(Patient, Patient).generate(n)
        for user in users:
            user.specialize(Patient, patient_id=user.user_id)
        return users

    def sql(self):
        new_sql = f"INSERT INTO {TABLE_PATIENT} VALUES (" \
                  f"{self.user_id}" \
                  f");\n"
        return super(Patient, self).sql() + new_sql


class WorkingStaff(User):
    def __init__(self):
        super(WorkingStaff, self).__init__()
        self.working_staff_id = self.user_id  # really smart approach
        self.salary = None
        self.schedule = None
        self.qualification = None

    @staticmethod
    def generate(n):
        users = super(WorkingStaff, WorkingStaff).generate(n)
        for user in users:
            user.specialize(WorkingStaff, working_staff_id=user.user_id, salary=None, schedule=None, qualification=None)
        return users

    def sql(self):
        new_sql = f"INSERT INTO {TABLE_WORKING_STAFF} VALUES(" \
                  f"{self.user_id}, {self.salary}, NULL, NULL, '{self.qualification}');\n"
        return super(WorkingStaff, self).sql() + new_sql


class Doctor(WorkingStaff):
    def __init__(self):
        super(Doctor, self).__init__()
        self.doctor_id = self.user_id

    @staticmethod
    def generate(n):
        users = super(Doctor, Doctor).generate(n)
        for user in users:
            user.specialize(Doctor, doctor_id=user.user_id, salary=random.randint(40, 120) * 50,
                            qualification=f"Qualification {random.randint(1, 50)}")
        return users

    def sql(self):
        new_sql = f"INSERT INTO {TABLE_DOCTOR} VALUES (" \
                  f"{self.user_id});\n"
        return super(Doctor, self).sql() + new_sql


class Nurse(WorkingStaff):
    def __init__(self):
        super(WorkingStaff, self).__init__()
        self.doctor_id = self.user_id
        self.doctor_team = None

    @staticmethod
    def generate(n):
        users = super(Nurse, Nurse).generate(n)
        for user in users:
            user.specialize(Nurse, doctor_id=user.user_id, doctor_team=random.randint(1, DOCTOR_NUMBER),
                            salary=random.randint(40, 120) * 50)
        return users

    def sql(self):
        new_sql = f"INSERT INTO {TABLE_NURSE} VALUES (" \
                  f"{self.user_id}, {self.doctor_team});\n"
        return super(Nurse, self).sql() + new_sql


class Accountant(WorkingStaff):
    def __init__(self):
        super(WorkingStaff, self).__init__()
        self.accountant_id = self.user_id
        self.license_id = None

    @staticmethod
    def generate(n):
        pool = GeneralPool()
        users = super(Accountant, Accountant).generate(n)
        for user in users:
            user.specialize(Accountant, accountant_id=user.user_id, license_id=pool.get("AccountantLicense"))
        return users

    def sql(self):
        new_sql = f"INSERT INTO {TABLE_ACCOUNTANT} VALUES(" \
                  f"{self.user_id}, {self.license_id});\n"
        return super(Accountant, self).sql() + new_sql


class Pharmacist(WorkingStaff):
    def __init__(self):
        super().__init__()
        self.pharmacist_id = self.user_id
        self.license_id = None

    @staticmethod
    def generate(n):
        pool = GeneralPool()
        users = super(Pharmacist, Pharmacist).generate(n)
        for user in users:
            user.specialize(Accountant, pharmacist_id=user.user_id, license_id=pool.get("PharmacistLicense"))
        return users

    def sql(self):
        new_sql = f"INSERT INTO {TABLE_PHARMACIST} VALUES (" \
                  f"{self.user_id}, {self.license_id});\n"
        return super(Pharmacist, self).sql() + new_sql


class DoctorTeam:
    def __init__(self, doctor_team_id_, doctor_id_):
        self.doctor_team_id = doctor_team_id_
        self.doctor_id = doctor_id_

    @staticmethod
    def generate(n):
        dteams = []
        for i in range(n):
            dteams.append(DoctorTeam(i + 1, i + 1))
        return dteams

    def sql(self):
        return f"INSERT INTO {TABLE_DOCTOR_TEAM} VALUES (" \
               f"{self.doctor_team_id}, {self.doctor_id});\n"


class Notification:
    def __init__(self, date_=None, title_=None, content_=None, user_id_=None):
        self.id = None
        self.date = date_
        self.title = title_
        self.content = content_
        self.user_id = user_id_

    def sql(self):
        return f"INSERT INTO {TABLE_NOTIFICATION} VALUES(" \
               f"{self.id}, '{str(self.date)}', '{self.title}'," \
               f" '{self.content}', {self.user_id});\n"


class InvoiceBill:
    def __init__(self, id_=None, date_=None, price_=None, created_by_=None, is_paid_=None):
        self.id = id_
        self.date = date_
        self.price = price_
        self.created_by = created_by_
        self.is_paid = is_paid_

    def sql(self):
        return f"INSERT INTO {TABLE_INVOICE_BILL} VALUES(" \
               f"'{self.date}', {self.price}, {self.created_by}, {self.is_paid});\n"


class MedicalRecord:
    def __init__(self, id_=None, description_=None, date_=None, appointment_id_=None, created_by_=None):
        self.id = id_  # we do not use it in inserts
        self.description = description_
        self.date = date_
        self.appointment_id = appointment_id_
        self.created_by = created_by_

    def sql(self):
        return f"INSERT INTO {TABLE_MEDICAL_RECORD} VALUES(" \
               f"'{self.description}', '{self.date}', {self.appointment_id}, {self.created_by});\n"

    @staticmethod
    def generate(n, date, appointment_id, dteam):
        medical_records = []
        for i in range(n):
            mr = MedicalRecord()
            mr.description = f"Medical recored description {random.randint(1, 1000)}."
            mr.date = date
            mr.appointment_id = appointment_id
            mr.created_by = dteam
            medical_records.append(mr)
        return medical_records


class Appointment:
    def __init__(self):
        self.id = None
        self.room = None
        self.type = None  # 0 - hospital, 1 - home visit
        self.date = None
        self.start_time = None
        self.end_time = None
        self.patient_id = None
        self.doctor_team_id = None
        self.invoice_bill_id = None
        self.notifications = []  # this is used only in code
        self.invoice_bills = []  # this is used only in code
        self.medical_records = []

    @staticmethod
    def generate(n, patient, dteams: DoctorTeam):
        pool = AppointmentIDPool()
        appointments = []
        for i in range(n):
            dteam = random.choice(dteams)
            app = Appointment()
            app.id = pool.get()
            app.room = random.randint(100, 500)
            app.type = random.randint(0, 1)
            app.doctor_team_id = dteam.doctor_team_id
            app.start_time = gen_datetime(start=datetime.datetime(2006, 1, 1))
            app.end_time = app.start_time + datetime.timedelta(minutes=15)
            app.patient_id = patient.patient_id

            # generate notifications for the appointment
            notif_time = app.start_time - datetime.timedelta(minutes=15)
            title = APPOINTMENT_NOTIFICATION_TITLE
            content = APPOINTMENT_NOTIFICATION_CONTENT.format(id=app.id, room=app.room)
            app.notifications.append(Notification(notif_time, title, content, dteam.doctor_id))
            app.notifications.append(Notification(notif_time, title, content, app.patient_id))

            # generate invoice bill
            acc_id = random.randint(1, ACCOUNTANT_NUMBER)
            app.invoice_bills.append(InvoiceBill(None, app.end_time,
                                                 random.randint(1, 20) * 50, acc_id,
                                                 random.choice([True, False])))

            app.medical_records.extend(MedicalRecord.generate(1, app.end_time, app.id, app.doctor_team_id))
            appointments.append(app)
        return appointments

    def sql(self):
        appointment_sql = f"INSERT INTO {TABLE_APPOINTMENT} VALUES(" \
                          f"{self.id}, {self.room}, {self.type}, " \
                          f"'{self.start_time}', '{self.end_time}', {self.patient_id}, " \
                          f"{self.doctor_team_id}, {self.invoice_bill_id});\n"
        notif_sql = "".join([notif.sql() for notif in self.notifications])
        inv_bill_sql = "".join([inv.sql() for inv in self.invoice_bills])
        mr_sql = "".join([mr.sql() for mr in self.medical_records])

        return appointment_sql + notif_sql + inv_bill_sql + mr_sql
