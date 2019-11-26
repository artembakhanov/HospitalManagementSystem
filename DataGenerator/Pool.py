from random import shuffle

from DataGenerator.static import *
from DataGenerator.config import *


def inheritors(cls):
    """
    Finds all descendant classes of a given class.
    Taken from: https://stackoverflow.com/questions/5881873/python-find-all-classes-which-inherit-from-this-one
    :param cls: class, which descendants one wants to find
    :return:
    """
    subclasses = set()
    work = [cls]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.add(child)
                work.append(child)
    return subclasses


class Singleton:
    """
    Abstract class that allows to create only
    one instance of a class in run time.
    """
    _initialized = False

    def __new__(cls, *args, **kwargs):
        """
        Redefine __new__ for creating single object.
        :param cls: the class itself
        :return: instance of the class
        """
        if not hasattr(cls, 'instance'):
            print("Creating: " + str(cls))
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        if not self._initialized:
            self._initialized = True


class Pool(Singleton):
    """
    An abstract class that represents a pool of some values.

    It is a singleton because the pool can be created
    from several parts of code and it needs to be
    the only one instance (data need to be unique).
    """
    _name = None
    _data = None  # data are stored here

    def __init__(self):
        if not self._initialized:
            print(f"Calling init from: {self.__class__}")
            self.init_data()
        super().__init__()

    def _get_data(self):
        with open(self._name, 'r', encoding='utf-8') as f:
            return f.read().splitlines()

    def get(self):
        return None if len(self._data) == 0 else self._data.pop()

    def init_data(self):
        self._data = self._get_data()
        shuffle(self._data)


class AddressPool(Pool):

    def __init__(self):
        self._name = ADDRESS_SET_FILE
        super().__init__()


class FNamePool(Pool):

    def __init__(self):
        self._name = FNAME_SET_FILE
        super().__init__()


class LNamePool(Pool):

    def __init__(self):
        self._name = LNAME_SET_FILE
        super().__init__()


class EmailPool(Pool):
    def __init__(self):
        self._name = EMAIL_SET_FILE
        super().__init__()


class PhonePool(Pool):
    def __init__(self):
        self._name = PHONE_SET_FILE
        super().__init__()


class PasswordPool(Pool):
    def __init__(self):
        self._name = PASSWORD_SET_FILE
        super().__init__()


class UserIDPool(Pool):
    def init_data(self):
        self._data = list(reversed([i for i in range(1, 100001)]))


class WorkingStaffIDPool(Pool):
    def init_data(self):
        self._data = list(reversed([i for i in range(1, USER_NUMBER)]))


class AppointmentIDPool(Pool):
    def init_data(self):
        self._data = list(reversed([i for i in range(1, 100001)]))


class LicensePool(Pool):
    """
    An abstract pool that is used to generate
    different types of licenses.
    """

    def init_data(self):
        self._data = [i for i in range(10 ** 5, 10 ** 6)]
        shuffle(self._data)


class AccountantLicensePool(LicensePool):
    pass


class PharmacistLicensePool(LicensePool):
    pass


class SlotPool(Pool):
    """
    Slot pool. Be careful:
    is is used with side-effects.
    """
    data = []
    _data = data

    def __init__(self):
        pass

    def _get_data(self):
        pass


class DoctorRoomPool(Pool):
    def init_data(self):
        self._data = [i for i in range(1, DOCTOR_NUMBER + 1)]
        shuffle(self._data)


class GeneralPool(Singleton):
    """
    It is a pool that unifies all the possible pools.

    They are instantiated automatically and used as
    a private attributes. In order to get some data
    use get(str), where str - what you want to get.
    """

    def __init__(self):
        super().__init__()

        # get all pools
        subs = inheritors(Pool)

        for sub in subs:
            # create instance of a pool and set it as an attribute
            self.__setattr__("_" + sub.__name__.lower(), sub())

    def get(self, name):
        """
        Get something from general pool.
        :param name: what one wants to get.
        Possible values: email, fname, lname, address, phone, password, userID, AccountantLicense, PharmacistLicense,
        AppointmentID, slot, DoctorRoom
        (Not case sensitive).
        :return: random value of what is requested
        """
        return self.__getattribute__(f"_{name.lower()}pool").get()

    def reset(self):
        """
        Reset the general pool.

        It means that all the data are generated (or read) again.
        After calling this function do not use generated data with
        what you generated before calling it. It is GUARANTEED that
        the data are NOT unique.
        """
        super().__init__()
        subs = inheritors(Pool)
        for sub in subs:
            # print(sub)
            name = "_" + sub.__name__.lower()
            self.__setattr__(name, sub())
            self.__getattribute__(name)._initialized = False


if __name__ == "__main__":
    sos = GeneralPool()
    sos1 = GeneralPool()

    print(sos.get("email"))
