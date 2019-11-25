import datetime
import random

from DataGenerator.Pool import SlotPool
from DataGenerator.config import *
from DataGenerator.static import *


class TimeSlot:
    def __init__(self, doctor_team_id=None, start_=None, end_=None, room_=None):
        self.doctor_team_id = doctor_team_id
        self.start = start_
        self.end = end_
        self.room = room_


class DoctorTeam:
    def __init__(self, doctor_team_id_, doctor_id_):
        self.doctor_team_id = doctor_team_id_
        self.doctor_id = doctor_id_

    @staticmethod
    def generate(n, doctors):
        """
        Side effect warning!!!
        This method also generates all possible time slots
        starting from doctor hire date until current date.

        :param n: the number of doctor teams
        :param doctors: list of all doctors
        :return: list of doctor teams
        """
        pool = SlotPool()
        dteams = []
        for i in range(n):
            dteams.append(DoctorTeam(i + 1, i + 1))
            DoctorTeam._add_time_slots(doctors[i], i + 1)
        random.shuffle(pool.data)
        return dteams

    @staticmethod
    def _add_time_slots(doctor, doctor_team_id):
        pool = SlotPool()
        now = datetime.datetime.now()
        cur = doctor.hire_date

        # everyone works from START_WORKING_HOUR
        cur = cur.replace(hour=START_WORKING_HOUR, minute=0, second=0, microsecond=0)
        while cur < now:
            # working only from Monday to Friday
            # https://docs.python.org/3/library/datetime.html#datetime.date.weekday
            if 0 <= cur.weekday() <= 4:
                for i in range(MAX_SLOTS_PER_DAY):
                    start_time = cur + i * datetime.timedelta(minutes=SLOT_DURATION)
                    pool.data.append(
                        TimeSlot(doctor_team_id, start_time, start_time + datetime.timedelta(minutes=15), doctor.room))
            cur += datetime.timedelta(days=1)

    def sql(self):
        return f"INSERT INTO {TABLE_DOCTOR_TEAM} {VALUES_DOCTOR_TEAM} VALUES (" \
               f"{self.doctor_id});\n"
