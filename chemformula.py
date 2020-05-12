from formulaparser import parse_formula
from mole import molar_mass


class Component:

    def __init__(self, count, symbol, mass_percent):
        self.count = int(count)
        self.symbol = symbol
        self.mass_percent = mass_percent

    def __str__(self):
        return self.symbol + "(" + str(self.count) + "," + str(self.mass_percent) + ")"

    def __eq__(self, other):
        if not isinstance(other, Component):
            return False
        return self.count == other.count and \
               self.symbol == other.symbol and \
               self.mass_percent == other.mass_percent


def composition(formula: str) -> list:
    _composition = parse_formula(formula)
    _molar_mass = molar_mass(formula)
    _components = []
    for count, symbol in _composition:
        _mass_percent = molar_mass(symbol)/_molar_mass
        _mass_percent = _mass_percent.value.decimal() * int(count)
        _mass_percent = round(_mass_percent * 100, 2)
        _components.append(Component(count, symbol, _mass_percent))

    return _components