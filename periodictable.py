class Element:

    def __init__(self, atomic_number, symbol, name, atomic_mass):
        self.atomic_number = atomic_number
        self.symbol = symbol
        self.name = name
        self.atomic_mass = atomic_mass

    def __str__(self):
        return f"{name} ({atomic_number}, {symbol}, {atomic_mass})"

if __name__ == '__main__':
    data_file = open("periodic-table.dat", "r")
    data = data_file.read()
    lines = data.split("\n")
    for line in lines:
        field = line.split(",")
        atomic_number, symbol, name, atomic_mass = field
        element = Element(atomic_number, symbol, name, atomic_mass)
        print(element)