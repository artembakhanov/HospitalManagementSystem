from DataGenerator.Type import DoctorTeam
from DataGenerator.config import DOCTOR_NUMBER


def generate():
    return DoctorTeam.generate(DOCTOR_NUMBER)
