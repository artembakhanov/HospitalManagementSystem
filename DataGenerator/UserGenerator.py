from DataGenerator.Type import Patient, Doctor, Nurse, Pharmacist, Accountant
from DataGenerator.config import DOCTOR_NUMBER, PATIENT_NUMBER, NURSE_NUMBER, PHARMACIST_NUMBER, ACCOUNTANT_NUMBER


def generate():
    users = []
    users.extend(Patient.generate(PATIENT_NUMBER))
    users.extend(Doctor.generate(DOCTOR_NUMBER))
    users.extend(Nurse.generate(NURSE_NUMBER))
    users.extend(Pharmacist.generate(PHARMACIST_NUMBER))
    users.extend(Accountant.generate(ACCOUNTANT_NUMBER))
    return users
