import datetime
import random

from DataGenerator.DateGenerator import gen_datetime
from DataGenerator.Pool import GeneralPool, SlotPool
from DataGenerator.config import *
from static import *

MIDDLE_NAME_CHANCE = 0.5
BLOCKED_CHANCE = 0.003


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
        self.role = ROLE_USER
        self.blocked_by = None

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
            if random.random() <= BLOCKED_CHANCE:
                user.blocked_by = random.randint(1, ADMIN_NUMBER)
            user.gender = "M" if random.random() >= 0.5 else "F"
            user.birth_date = None  # TODO: make birthdate generator
            users.append(user)

        return users

    def specialize(self, cls, **kwargs):
        self.__class__ = cls
        for key, value in kwargs.items():
            self.__setattr__(key, value)

    def sql(self):
        return f"INSERT INTO {TABLE_USER} {VALUES_USER}" \
               f"VALUES ('{self.email}', " \
               f"'{self.fname}', '{self.lname}', " \
               f"'{self.mname}', '{self.gender}', " \
               f"'{self.birth_date}', '{self.address}', " \
               f"{self.role}, '{self.password_hash}'," \
               f"NULL);\n" + \
               (f"INSERT INTO {TABLE_BLOCKED}  {VALUES_BLOCKED} VALUES({self.user_id}, {self.blocked_by});\n" if self.blocked_by else "")


class Patient(User):
    def __init__(self):
        super(Patient, self).__init__()
        self.patient_id = None
        self.role += ROLE_PATIENT

    @staticmethod
    def generate(n):
        users = super(Patient, Patient).generate(n)
        for i, user in enumerate(users):
            user.role += ROLE_PATIENT
            user.specialize(Patient, patient_id=i + 1)
        return users

    def sql(self):
        new_sql = f"INSERT INTO {TABLE_PATIENT} {VALUES_PATIENT} VALUES (" \
                  f"{self.user_id}" \
                  f");\n"
        return super(Patient, self).sql() + new_sql


class Schedule:
    def __init__(self, id_=None, week_day_=None, start_time_=None, end_time_=None):
        self.id = id_
        self.week_day = week_day_
        self.start_time = start_time_
        self.end_time = end_time_

    @staticmethod
    def generate():
        schedule = []
        for i in range(1, 6):
            schedule.append(Schedule(week_day_=i, start_time_=datetime.time(START_WORKING_HOUR),
                                     end_time_=datetime.time(END_WORKING_HOUR)))

        return schedule

    def sql(self):
        return f"INSERT INTO {TABLE_SCHEDULE} {VALUES_SCHEDULE} VALUES(" \
               f"{self.week_day}, '{self.start_time}', '{self.end_time}');\n"


class WorkingStaff(User):
    def __init__(self):
        super(WorkingStaff, self).__init__()
        self.working_staff_id = None # really smart approach
        self.salary = None
        self.schedule = None
        self.qualification = None
        self.hire_date = None

    @staticmethod
    def generate(n):
        users = super(WorkingStaff, WorkingStaff).generate(n)
        for i, user in enumerate(users):
            user.role += 0 # todo: cock
            user.specialize(WorkingStaff,
                            working_staff_id=i + 1,
                            salary=None,
                            schedule=[1, 2, 3, 4, 5],
                            qualification=f"Qualification {random.randint(1, 500)}",
                            # this is really interesting kostyl, text me if you can not get it
                            hire_date=gen_datetime(datetime.datetime(HOSPITAL_START_YEAR, 1, 1),
                                                   datetime.datetime(2018, 1, 1)))
        return users

    def sql(self):
        new_sql = f"INSERT INTO {TABLE_WORKING_STAFF} {VALUES_WORKING_STAFF} VALUES(" \
                  f"{self.user_id}, {self.salary}, '{self.qualification}');\n"
        schedule_sql = "".join([f"INSERT INTO {TABLE_STAFF_SCHEDULE}  {VALUES_STAFF_SCHEDULE} VALUES({self.working_staff_id}, {i});\n"
                                for i in self.schedule])
        return super(WorkingStaff, self).sql() + new_sql + schedule_sql


class Admin(WorkingStaff):
    def __init__(self):
        super(Admin, self).__init__()
        self.admin_id = None

    @staticmethod
    def generate(n):
        users = super(Admin, Admin).generate(n)
        pool = GeneralPool()
        for user in users:
            user.specialize(Admin, admin_id=None)

    def sql(self):
        new_sql = f"INSERT INTO {TABLE_ADMIN} {VALUES_ADMIN} VALUES(" \
                f"{self.working_staff_id});\n"
        return super(Admin, self).sql() + new_sql


class Doctor(WorkingStaff):
    def __init__(self):
        super(Doctor, self).__init__()
        self.doctor_id = self.user_id
        self.room = None

    @staticmethod
    def generate(n):
        users = super(Doctor, Doctor).generate(n)
        pool = GeneralPool()
        for user in users:
            user.specialize(Doctor, doctor_id=user.user_id, salary=random.randint(40, 120) * 50,
                            qualification=f"Qualification {random.randint(1, 50)}", room=pool.get("DoctorRoom"))
        return users

    def sql(self):
        new_sql = f"INSERT INTO {TABLE_DOCTOR} VALUES (" \
                  f"{self.working_staff_id}, {self.room});\n"
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
                  f"{self.working_staff_id}, {self.doctor_team});\n"
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
                  f"{self.working_staff_id}, {self.license_id});\n"
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
                  f"{self.working_staff_id}, {self.license_id});\n"
        return super(Pharmacist, self).sql() + new_sql


class TimeSlot:
    def __init__(self, doctor_team_id=None, start_=None, end_=None):
        self.doctor_team_id = doctor_team_id
        self.start = start_
        self.end = end_


class DoctorTeam:
    def __init__(self, doctor_team_id_, doctor_id_):
        self.doctor_team_id = doctor_team_id_
        self.doctor_id = doctor_id_

    @staticmethod
    def generate(n, doctors):
        """
        Side effect warning!!!
        This method also generates all possible time slots
        starting from doctor hire date until current date.

        :param n: the number of doctor teams
        :param doctors: list of all doctors
        :return: list of doctor teams
        """
        pool = SlotPool()
        dteams = []
        for i in range(n):
            dteams.append(DoctorTeam(i + 1, i + 1))
            DoctorTeam._add_time_slots(doctors[i], i + 1)
        random.shuffle(pool.data)
        return dteams

    @staticmethod
    def _add_time_slots(doctor, doctor_team_id):
        pool = SlotPool()
        now = datetime.datetime.now()
        cur = doctor.hire_date

        # everyone works from START_WORKING_HOUR
        cur = cur.replace(hour=START_WORKING_HOUR, minute=0, second=0, microsecond=0)
        while cur < now:
            # working only from Monday to Friday
            # https://docs.python.org/3/library/datetime.html#datetime.date.weekday
            if 0 <= cur.weekday() <= 4:
                for i in range(MAX_SLOTS_PER_DAY):
                    start_time = cur + i * datetime.timedelta(minutes=SLOT_DURATION)
                    pool.data.append(TimeSlot(doctor_team_id, start_time, start_time + datetime.timedelta(minutes=15)))
            cur += datetime.timedelta(days=1)

    def sql(self):
        return f"INSERT INTO {TABLE_DOCTOR_TEAM} {VALUES_DOCTOR_TEAM} VALUES (" \
               f"{self.doctor_id});\n"


class Notification:
    def __init__(self, date_=None, title_=None, content_=None, user_id_=None):
        self.id = None
        self.date = date_
        self.title = title_
        self.content = content_
        self.user_id = user_id_

    def sql(self):
        return f"INSERT INTO {TABLE_NOTIFICATION} VALUES(" \
               f"'{str(self.date)}', '{self.title}'," \
               f" '{self.content}', {self.user_id});\n"


class InvoiceBill:
    def __init__(self, id_=None, date_=None, price_=None, created_by_=None, is_paid_=None):
        self.id = id_
        self.date = date_
        self.price = price_
        self.created_by = created_by_
        self.is_paid = is_paid_

    def sql(self):
        return f"INSERT INTO {TABLE_INVOICE_BILL} {VALUES_INVOICE_BILL} VALUES(" \
               f"'{self.date}', {self.price}, {self.created_by}, {self.is_paid});\n"


class Prescription:
    def __init__(self):
        self.id = None
        self.medicals = []

    def sql(self):
        medicals_sql = "".join([medical.sql() for medical in self.medicals])
        return medicals_sql + f"INSERT INTO {TABLE_PRESCRIPTION} {VALUES_PRESCRIPTION} VALUES();\n"


class MedicalRecord:
    def __init__(self, id_=None, description_=None, date_=None, appointment_id_=None, created_by_=None):
        self.id = id_  # we do not use it in inserts
        self.description = description_
        self.date = date_
        self.appointment_id = appointment_id_
        self.created_by = created_by_
        self.prescription = None

    def sql(self):
        return f"INSERT INTO {TABLE_MEDICAL_RECORD} {VALUES_MEDICAL_RECORD} VALUES(" \
               f"'{self.description}', '{self.date}', {self.appointment_id}, {self.created_by});\n"

    @staticmethod
    def generate(n, date, appointment_id, dteam):
        medical_records = []
        for i in range(n):
            mr = MedicalRecord()
            mr.description = f"Medical record description {random.randint(1, 1000)}."
            mr.date = date
            mr.appointment_id = appointment_id
            mr.created_by = dteam
            mr.prescription = Prescription()
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
        pool = GeneralPool()
        appointments = []
        for i in range(n):
            dteam = random.choice(dteams)
            app = Appointment()
            app.id = pool.get("AppointmentID")
            app.room = random.randint(100, 500)
            app.type = random.randint(0, 1)

            # getting a free slot
            slot = pool.get("slot")
            app.start_time = slot.start
            app.end_time = slot.end
            app.doctor_team_id = slot.doctor_team_id
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
        appointment_sql = f"INSERT INTO {TABLE_APPOINTMENT} {VALUES_APPOINTMENT} VALUES(" \
                          f" {self.room}, {self.type}, " \
                          f"'{self.start_time}', '{self.end_time}', {self.patient_id}, " \
                          f"{self.doctor_team_id}, {self.invoice_bill_id});\n"
        notif_sql = "".join([notif.sql() for notif in self.notifications])
        inv_bill_sql = "".join([inv.sql() for inv in self.invoice_bills])
        mr_sql = "".join([mr.sql() for mr in self.medical_records])

        return appointment_sql + notif_sql + inv_bill_sql + mr_sql
