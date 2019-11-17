from random import shuffle


class Singleton:
    def __new__(cls, *args, **kwargs):
        """
        Redefine __new__ for creating single object.
        :param cls: the class itself
        :return: instance of the class
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


class Pool(Singleton):
    _name = None

    def __init__(self):
        self._data = self._get_data()
        shuffle(self._data)

    def _get_data(self):
        with open(self._name, 'r', encoding='utf-8') as f:
            return f.read().splitlines()

    def get(self, n: int = 1):
        return None if len(self._data) == 0 else self._data.pop()


class AddressPool(Pool):
    """
    This is a singleton that stores all available emails.
    Emails are static and were generated with some script.
    They are stored in a file (one email on a single line).
    """

    def __init__(self):
        self._name = "address.txt"
        super().__init__()


class FNamePool(Pool):
    def __init__(self):
        self._name = "first_names.all.txt"
        super().__init__()


class LNamePool(Pool):
    def __init__(self):
        self._name = "last_names.all.txt"
        super().__init__()


class EmailPool(Pool):
    def __init__(self):
        self._name = "email.txt"
        super().__init__()


class PhonePool(Pool):
    def __init__(self):
        self._name = "phone.txt"
        super().__init__()


class PasswordPool(Pool):
    def __init__(self):
        self._name = "password.txt"
        super().__init__()


class GeneralPool(Singleton):

    def __init__(self):
        subs = Pool.__subclasses__()
        for sub in subs:
            self.__setattr__("_" + sub.__name__.lower(), sub())

    def get(self, name):
        """
        Get something from general pool.
        :param name: what one wants to get. Possible values: email, fname, lname, address, phone, password
        :return: random value of what is requested
        """
        return self.__getattribute__(f"_{name}pool").get()


if __name__ == "__main__":
    sos = GeneralPool()
    print(sos.get("email"))
