import inspect
import os
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from DataGenerator import UserGenerator, DoctorTeamGenerator, AppointmentGenerator


class DataGenerator:
    def __init__(self):
        self.sql = []
        pass

    def generate(self):
        """
        This function generates a bunch of queries for the database with randomly generated data.
        :return: a string with queries
        """
        queries = []
        self.generate_users()
        self.generate_doctor_teams()
        self.generate_appointments(self.users)

    def generate_users(self):
        self.users = UserGenerator.generate()
        self.sql.extend([user.sql() for user in self.users])

    def generate_doctor_teams(self):
        self.dteams = DoctorTeamGenerator.generate()
        self.sql.extend([team.sql() for team in self.dteams])

    def generate_appointments(self, users):
        self.appointments = AppointmentGenerator.generate(self.users, self.dteams)
        self.sql.extend([app.sql() for app in self.appointments])

    def generate_messages(self):
        """
        Also generates notifications for each message.
        """
        pass


if __name__ == "__main__":
    print(DataGenerator().generate())
