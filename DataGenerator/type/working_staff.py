import datetime
import random

from DataGenerator.DateGenerator import gen_datetime
from DataGenerator.Pool import GeneralPool
from DataGenerator.config import *
from DataGenerator.static import *
from DataGenerator.type import User


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
        self.working_staff_id = None  # really smart approach
        self.salary = 2000
        self.schedule = None
        self.qualification = None
        self.hire_date = None

    @staticmethod
    def generate(n):
        pool = GeneralPool()
        users = super(WorkingStaff, WorkingStaff).generate(n)
        for i, user in enumerate(users):
            user.role += ROLE_WORKING_STAFF  # todo: cock
            user.specialize(WorkingStaff,
                            working_staff_id=pool.get("WorkingStaffID"),
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
        schedule_sql = "".join(
            [f"INSERT INTO {TABLE_STAFF_SCHEDULE}  {VALUES_STAFF_SCHEDULE} VALUES({self.working_staff_id}, {i});\n"
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
            user.role += ROLE_ADMIN
            user.specialize(Admin, admin_id=None, salary=random.randint(4, 10) * 250)
        return users

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
            user.role += ROLE_DOCTOR
            user.specialize(Doctor, doctor_id=user.user_id, salary=random.randint(40, 120) * 50,
                            qualification=f"Qualification {random.randint(1, 50)}", room=pool.get("DoctorRoom"))
        return users

    def sql(self):
        new_sql = f"INSERT INTO {TABLE_DOCTOR} {VALUES_DOCTOR} VALUES (" \
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
            user.role += ROLE_NURSE
            user.specialize(Nurse, doctor_id=user.user_id, doctor_team=random.randint(1, DOCTOR_NUMBER),
                            salary=random.randint(40, 120) * 50)
        return users

    def sql(self):
        new_sql = f"INSERT INTO {TABLE_NURSE} {VALUES_NURSE} VALUES (" \
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
            user.role += ROLE_ACCOUNTANT
            user.specialize(Accountant,
                            accountant_id=user.user_id,
                            license_id=pool.get("AccountantLicense"),
                            salary=random.randint(4, 5) * 250)
        return users

    def sql(self):
        new_sql = f"INSERT INTO {TABLE_ACCOUNTANT} {VALUES_ACCOUNTANT} VALUES(" \
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
            user.role += ROLE_PHARMACIST
            user.specialize(Pharmacist, pharmacist_id=user.user_id, license_id=pool.get("PharmacistLicense"),
                            salary=random.randint(5, 10) * 200)
        return users

    def sql(self):
        new_sql = f"INSERT INTO {TABLE_PHARMACIST} {VALUES_PHARMACIST} VALUES (" \
                  f"{self.working_staff_id}, {self.license_id});\n"
        return super(Pharmacist, self).sql() + new_sql
