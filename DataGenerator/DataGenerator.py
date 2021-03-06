import inspect
import os
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from DataGenerator.generator import AppointmentGenerator, UserGenerator, DoctorTeamGenerator
from DataGenerator.type import Doctor, Schedule, GeneralPool


class DataGenerator:
    """
    Generator for all the data that will be inserted to the database for testing.
    """

    def __init__(self):
        self.sql = []  # all queries are stored here
        pass

    def generate(self):
        """
        This function generates a bunch of queries for the database with randomly generated data.
        :return: a string with queries
        """
        self.sql = []

        self._generate_schedule()
        print("schedules have been generated")
        self._generate_users()  # without nurses
        print("users have been generated")
        self._generate_doctor_teams()
        print("doctors teams have been generated")
        self._generate_nurses()
        print("nurses teams have been generated")
        self._generate_appointments()
        print("appointments have been generated")

        GeneralPool().reset()
        return self.sql

    def _generate_users(self):
        """
        Generates all users, including patients, working staff, etc.
        """
        self.users = UserGenerator.generate()
        self.sql.extend([user.sql() for user in self.users])

    def _generate_doctor_teams(self):
        """
        Generate doctor teams.
        """
        doctors = [user for user in self.users if user.__class__ == Doctor]
        self.dteams = DoctorTeamGenerator.generate(doctors)
        self.sql.extend([team.sql() for team in self.dteams])

    def _generate_nurses(self):
        self.nurses = UserGenerator.generate_nurses()
        self.sql.extend([nurse.sql() for nurse in self.nurses])

    def _generate_appointments(self):
        """
        Generates appointments, invoices, notifications about appointments, and medical records.
        :param users: all users that have already been generated
        """
        self.appointments = AppointmentGenerator.generate(self.users, self.dteams)
        self.sql.extend([app.sql() for app in self.appointments])

    def _generate_messages(self):
        """
        Generate messages. Also generates notifications for each message.
        """
        pass

    def _generate_schedule(self):
        self.schedule = Schedule.generate()
        self.sql.extend([sch.sql() for sch in self.schedule])


if __name__ == "__main__":
    f = open("insertion.txt", "w+", encoding="utf-8")
    for x in DataGenerator().generate():
        f.write(x)
    f.close()
