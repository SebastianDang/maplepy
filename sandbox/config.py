import sys
import json

if sys.version_info >= (3, 4):
    import pathlib
    path = str(pathlib.Path(__file__).parent.absolute())
else:
    import os
    path = str(os.path.dirname(os.path.abspath(__file__)))


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

    def __init__(self, decorated):
        self._decorated = decorated

    def instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

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

    def __init__(self):
        print('Config:', 'Created', '.')

    def __setitem__(self, key, item):
        self.__args[key] = item

    def __getitem__(self, key):
        return self.__args[key]

    def init(self, filename):
        print('Config:', 'Initialized', '.')
        self.__filename = filename
        self.load()

    def load(self):
        print('Config:', 'Loading', self.__filename, '...')
        with open(path + "/" + self.__filename) as json_file:
            self.__args = json.load(json_file)

    def save(self):
        print('Config:', 'Saving', self.__filename, '...')
        with open(path + "/" + self.__filename, 'w') as json_file:
            json.dump(self.__args, json_file, indent=2)
