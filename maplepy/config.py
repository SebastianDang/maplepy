import json
import logging
import sys


class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Also, the decorated class cannot be
    inherited from. Other than that, there are no restrictions that apply
    to the decorated class.

    To get the singleton instance, use the `instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    """

    __instance = None

    def __init__(self, decorated):
        self._decorated = decorated

    def instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        try:
            if not self.__instance:
                self.__instance = self._decorated()
            return self.__instance
        except AttributeError:
            self.__instance = self._decorated()
            return self.__instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)


@Singleton
class Config:
    """
    A basic configuration helper class to manage different settings.
    """

    __args = {}

    def __setitem__(self, key, item):
        self.__args[key] = item

    def __getitem__(self, key):
        return self.__args.get(key)

    def init(self, filename):
        logging.info(f'[{filename}]')
        self.__filename = filename
        self.load()

    def load(self):
        logging.info(f'Loading: {self.__filename}')
        with open(self.__filename) as json_file:
            self.__args = json.load(json_file)

    def save(self):
        logging.info(f'Saving: {self.__filename}')
        with open(self.__filename, 'w') as json_file:
            json.dump(self.__args, json_file, indent=2)
