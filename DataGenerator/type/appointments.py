import datetime
import random

from DataGenerator.Pool import GeneralPool
from DataGenerator.config import *
from DataGenerator.type.doctors import DoctorTeam
from DataGenerator.type.notifications import Notification
from DataGenerator.static import *


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
            app.type = random.randint(0, 1)

            # getting a free slot
            slot = pool.get("slot")
            app.start_time = slot.start
            app.end_time = slot.end
            app.doctor_team_id = slot.doctor_team_id
            app.room = slot.room

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
            app.invoice_bill_id = app.id
            app.medical_records.extend(MedicalRecord.generate(1, app.end_time, app.id, app.doctor_team_id))
            appointments.append(app)
        return appointments

    def sql(self):
        appointment_sql = f"INSERT INTO {TABLE_APPOINTMENT} {VALUES_APPOINTMENT} VALUES(" \
                          f" {self.room}, {self.type}, " \
                          f"'{self.start_time}', '{self.end_time}', {self.patient_id}, " \
                          f"{self.doctor_team_id}, {self.invoice_bill_id});\n"
        notification_sql = "".join([notif.sql() for notif in self.notifications])
        invoice_bill_sql = "".join([inv.sql() for inv in self.invoice_bills])
        medical_record_sql = "".join([mr.sql() for mr in self.medical_records])

        return notification_sql + invoice_bill_sql + appointment_sql + medical_record_sql
