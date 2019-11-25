import datetime
import random

from DataGenerator.DateGenerator import gen_datetime
from DataGenerator.Pool import GeneralPool
from DataGenerator.config import *
from DataGenerator.static import *

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
            user.user_id = pool.get("UserID")
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
            user.birth_date = gen_datetime(datetime.datetime(START_BIRTHDATE_YEAR, 1, 1),
                                           datetime.datetime(END_BIRTHDATE_YEAR, 1, 1))
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
               f"{self.role}, '{self.password_hash}');\n" + \
               (
                   f"INSERT INTO {TABLE_BLOCKED}  {VALUES_BLOCKED} VALUES({self.user_id}, {self.blocked_by});\n" if self.blocked_by else "")


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
