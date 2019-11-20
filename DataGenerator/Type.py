import random

from DataGenerator.Pool import GeneralPool
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
