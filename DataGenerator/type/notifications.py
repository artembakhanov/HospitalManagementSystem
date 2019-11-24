import datetime
import random

from DataGenerator.DateGenerator import gen_datetime
from DataGenerator.Pool import GeneralPool, SlotPool
from DataGenerator.config import *
from static import *


class Notification:
    def __init__(self, date_=None, title_=None, content_=None, user_id_=None):
        self.id = None
        self.date = date_
        self.title = title_
        self.content = content_
        self.user_id = user_id_

    def sql(self):
        return f"INSERT INTO {TABLE_NOTIFICATION} {VALUES_NOTIFICATION} VALUES(" \
               f"'{str(self.date)}', '{self.title}'," \
               f" '{self.content}', {self.user_id});\n"
