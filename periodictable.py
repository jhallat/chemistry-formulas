import os

## TODO Probaly need to put this in a shared library
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Element(object):

    __slots__= ('atomic_number', 'symbol', 'name', 'atomic_mass')

    def __init__(self, atomic_number, symbol, name, atomic_mass):
        object.__setattr__(self, 'atomic_number', atomic_number)
        object.__setattr__(self, 'symbol', symbol)
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'atomic_mass', atomic_mass)

    def __setattr__(self, *args):
        raise AttributeError("Element is immutable")

    def __delattr__(self, *args):
        raise AttributeError("Element is immutable")


    def __str__(self):
        return f"{self.name} ({self.atomic_number}, {self.symbol}, {self.atomic_mass})"

class PeriodicTable(object, metaclass=Singleton):

    __slots__ = ("table_symbol", "table_number")

    def __init__(self):
        object.__setattr__(self, "table_symbol", {})
        object.__setattr__(self, "table_number", {})
        path = os.path.join(os.path.dirname(__file__), "periodic-table.dat")
        print(f"Initializing Periodic Table with data file '{path}'")
        data_file = open(path, "r")
        data = data_file.read()
        lines = data.split("\n")
        for line in lines:
            field = line.split(",")
            atomic_number, symbol, name, atomic_mass = field
            element = Element(atomic_number, symbol, name, atomic_mass)
            object.__getattribute__(self, "table_symbol")[symbol] = element
            object.__getattribute__(self, "table_number")[atomic_number] = element
        data_file.close()


    def __getattribute__(self, item):
        if not item == 'search':
            raise AttributeError("Cannot access internal tables of Periodic Table")
        return object.__getattribute__(self, 'search')

    def __delattr__(self, item):
        raise AttributeError("Periodic Table is immutable")

    def __setattr__(self, key, value):
        raise AttributeError("Periodic Table is immutable")

    def search(self, value):
        _value = str(value) if isinstance(value, int) else value
        if _value.isdigit():
            _table_number = object.__getattribute__(self, "table_number")
            if _value in _table_number:
                return _table_number[_value]
            else:
                message = f"Atomic number '{_value}' not found"
                raise Exception(message)
        else:
            _table_symbol = object.__getattribute__(self, "table_symbol")
            if _value in _table_symbol:
                return _table_symbol[_value]
            else:
                message = f"Symbol '{_value}' not found"
                raise Exception(message)



