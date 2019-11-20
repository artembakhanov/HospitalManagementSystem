import inspect
import os
import sys

from DataGenerator import UserGenerator, DoctorTeamGenerator

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)




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

    def generate_users(self):
        self.users = UserGenerator.generate()
        self.sql.extend([user.sql() for user in self.users])

    def generate_doctor_teams(self):
        self.dteams = DoctorTeamGenerator.generate()
        self.sql.extend([team.sql() for team in self.dteams])



if __name__ == "__main__":
    print(UserGenerator.generate())
    print(DataGenerator().generate_users())
