import datetime
import random

from DataGenerator.DateGenerator import gen_datetime
from DataGenerator.Pool import AppointmentIDPool
from DataGenerator.Type import Patient, DoctorTeam
from DataGenerator.config import *
from static import *


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
        self.notifications = []
        self.invoice_bills = []

    @staticmethod
    def generate(n, patient, dteams: DoctorTeam):
        pool = AppointmentIDPool()
        apps = []
        for i in range(n):
            dteam = random.choice(dteams)
            app = Appointment()
            app.id = pool.get()
            app.room = random.randint(100, 500)
            app.type = random.randint(0, 1)
            app.doctor_team_id = dteam.doctor_team_id
            app.start_time = gen_datetime(start=datetime.datetime(2006, 1, 1))
            app.end_time = app.start_time + datetime.timedelta(minutes=15)

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
        return apps

    def sql(self):
        appointment_sql = f"INSERT INTO {TABLE_APPOINTMENT} VALUES(" \
                          f"{self.id}, {self.room}, {self.type}, " \
                          f"'{self.start_time}', '{self.end_time}', {self.patient_id}, " \
                          f"{self.doctor_team_id}, {self.invoice_bill_id});\n"
        notif_sql = "".join([notif.sql() for notif in self.notifications])
        inv_bill_sql = "".join([inv.sql() for inv in self.invoice_bills])

        return appointment_sql + notif_sql + inv_bill_sql


def generate(users, dteams):
    apps = []
    patients = [user for user in users if user.__class__ == Patient]
    for patient in patients:
        appn = random.randint(0, MAX_APPOINTMENT_NUMBER)
        apps.extend(Appointment.generate(appn, patient, dteams))

    return apps
