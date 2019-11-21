import random

from DataGenerator.Type import Patient, Appointment
from DataGenerator.config import *


def generate(users, dteams):
    apps = []
    patients = [user for user in users if user.__class__ == Patient]
    for patient in patients:
        appn = random.randint(0, MAX_APPOINTMENT_NUMBER)
        apps.extend(Appointment.generate(appn, patient, dteams))

    return apps
