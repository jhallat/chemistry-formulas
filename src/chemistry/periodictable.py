import os
from collections import namedtuple

## TODO Probaly need to put this in a shared library
from enum import Enum


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]



Element = namedtuple('Element', ['atomic_number', 'symbol', 'name', 'atomic_mass'])
Ion = namedtuple('Ion', 'symbol name charge')

class PeriodicTable(object, metaclass=Singleton):

    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), "data/periodic-table.dat")
        with open(path, "r") as data_file:
            data = data_file.read()
            elements = [Element(*tuple(line.split(','))) for line in data.split('\n')]
            self._table_symbol = {element.symbol:element for element in elements}
            self._table_number = { element.atomic_number : element for element in elements }


    def __len__(self):
        return len(self._table_symbol)


    def __getitem__(self, item):
        if str(item).isnumeric():
            return self._table_number[str(item)]
        else:
            return self._table_symbol[item]

    def __contains__(self, item):
        if str(item).isnumeric():
            return str(item) in self._table_number
        else:
            return item in self._table_symbol

class Ions(object, metaclass=Singleton):

    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), "data/common-ions.dat")
        with open(path, "r") as data_file:
            data = data_file.read()
            ions = []
            for line in data.split('\n'):
                data_line = line.split(',')
                if len(data_line) == 3:
                    charge = int(data_line[2])
                else:
                    charge = [int(item) for item in data_line[2:]]
                ions.append(Ion(data_line[0], data_line[1], charge))
            self._ions = {ion.symbol: ion for ion in ions}
            self._names = {ion.name.replace('-',''): ion for ion in ions}
            self._stems = {self._stem(ion.name): ion for ion in ions}

    def _stem(self, name):
        if '-' in name:
            return name.split('-')[0]
        else:
            return name

    def __len__(self):
        return len(self._ions)

    def __getitem__(self, item):
        if item in self._ions:
            return self._ions[item]
        elif item in self._names:
            return self._names[item]
        elif item.endswith('ide'):
            return self._stems[item[0:-3]]

    def __contains__(self, item):
        if item in self._ions:
            return True
        elif item in self._names:
            return True
        elif item.endswith('ide'):
                return item[0:-3] in self._stems
        return False

class CommonCompounds(object, metaclass=Singleton):

    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), "data/common_compounds.dat")
        with open(path, "r") as data_file:
            data = data_file.read()
            compounds = [(item.split(',')[0], item.split(',')[1]) for item in data.split('\n')]
            self._symbols = {symbol: name for symbol, name in compounds}
            self._names = {name: symbol for symbol, name in compounds}

    def __getitem__(self, item):
        if item in self._symbols:
            return self._symbols[item]
        else:
            return self._names[item]

    def __contains__(self, item):
        return item in self._symbols or item in self._names
