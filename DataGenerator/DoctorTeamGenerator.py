from DataGenerator.type import DoctorTeam
from DataGenerator.config import DOCTOR_NUMBER


def generate(doctors):
    return DoctorTeam.generate(DOCTOR_NUMBER, doctors)
