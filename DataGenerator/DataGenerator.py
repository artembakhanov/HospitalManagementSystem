from DataGenerator.Pool import GeneralPool
import random

MIDDLE_NAME_CHANCE = 0.5

class UserGenerator:
    def __init__(self):
        pass

    def generate(self, n):
        pass


class User:
    def __init__(self):
        self.fname = None
        self.lname = None
        self.mname = ""
        self.email = None
        self.password_hash = None
        self.birth_date = None
        self.gender = None
        self.address = None

    @staticmethod
    def generate(n):
        pool = GeneralPool()
        users = []
        for i in range(n):
            user = User()
            user.email = pool.get("email")
            user.fname = pool.get("fname")
            user.lname = pool.get("fname")
            # user.mname = pool.get("mname") TODO: make this ...
            user.address = pool.get("address")
            user.password_hash = pool.get("password")
            if random.random() >= MIDDLE_NAME_CHANCE:
                user.mname = pool.get("fname")
            user.gender = "Male" if random.random() >= 0.5 else "Female"
            user.birth_date = None # TODO: make birthdate generator


