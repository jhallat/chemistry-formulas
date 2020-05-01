import os

class Element:

    def __init__(self, atomic_number, symbol, name, atomic_mass):
        self.atomic_number = atomic_number
        self.symbol = symbol
        self.name = name
        self.atomic_mass = atomic_mass

    def __str__(self):
        return f"{self.name} ({self.atomic_number}, {self.symbol}, {self.atomic_mass})"

class PeriodicTable:

    def __init__(self):
        self.table_symbol = {}
        self.table_number = {}
        data_file = open(os.path.join(os.path.dirname(__file__), "periodic-table.dat"), "r")
        data = data_file.read()
        lines = data.split("\n")
        for line in lines:
            field = line.split(",")
            atomic_number, symbol, name, atomic_mass = field
            element = Element(atomic_number, symbol, name, atomic_mass)
            self.table_symbol[symbol] = element
            self.table_number[atomic_number] = element
        data_file.close()

    def search(self, value):
        if value.isdigit():
            if value in self.table_number:
                return self.table_number[value]
            else:
                message = f"Atomic number '{value}' not found"
                raise Exception(message)
        else:
            if value in self.table_symbol:
                return self.table_symbol[value]
            else:
                message = f"Symbol '{value}' not found"
                raise Exception(message)



