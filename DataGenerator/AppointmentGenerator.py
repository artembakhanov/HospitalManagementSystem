import random


from DataGenerator.config import *
from DataGenerator.type import Patient, Appointment


def generate(users, dteams):
    apps = []
    patients = [user for user in users if user.__class__ == Patient]
    for patient in patients:
        appn = random.randint(0, MAX_APPOINTMENT_NUMBER)
        apps.extend(Appointment.generate(appn, patient, dteams))

    return apps
