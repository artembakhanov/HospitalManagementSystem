import datetime
import random


def gen_datetime(start=datetime.datetime(1900, 1, 1, 00, 00, 00), end=datetime.datetime.now()):
    return start + (end - start) * random.random()