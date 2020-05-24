from collections import namedtuple
from decimal import Decimal

from formulaparser import parse_formula
from measurement import Measurement, grams, validate_measurement, GRAMS, MOLES
from mole import molar_mass, moles_from_grams

Component = namedtuple("Component", "count symbol mass mass_percent")

class Composition:

    def __init__(self):
        self._components = []

    def __len__(self):
        return len(self._components)

    def __getitem__(self, item):
        if str(item).isnumeric():
            return self._components[item]
        else:
            return next(component for component in self._components if component.symbol == item)

    def __mul__(self, other):
        composition = Composition()
        for count, symbol, mass, mass_percent in self._components:
            mult_component = Component(count * other, symbol, mass * other, mass_percent)
            composition.append(mult_component)
        return composition

    def append(self, component):
        self._components.append(component)

    def __repr__(self):
        return str(self._components)

    def _formula(self):
        formula = ''
        for count, symbol, _, _ in self._components:
            formula += symbol
            formula += str(int(count)) if count != 1 else ''
        return formula

    def __format__(self, format_spec):
        if format_spec == 'f':
            return self._formula()
        else:
            #TODO return a more readable representation
            return str(self)

def _recursive_composition(_composition, _molar_mass, mass:Measurement = grams('1.000') ) -> [Component]:
    composition = Composition()
    for element in _composition:
        if isinstance(element, list):
            composition.append(_recursive_composition(element, _molar_mass, mass))
        else:
            count, symbol = element
            _mass_percent = molar_mass(symbol)/_molar_mass
            _mass_percent = _mass_percent.value.decimal() * int(count)
            _mass = mass * _mass_percent
            _mass_percent = round(_mass_percent * 100, 2)
            composition.append(Component(count, symbol, _mass, _mass_percent))

    return composition

def composition(formula: str, mass:Measurement = grams('1.000') ) -> [Component]:
    return _recursive_composition(parse_formula(formula), molar_mass(formula), mass)


def formula_from_percent(elements: [(str, Decimal)], molar_mass = None) -> str:
    """Creates the simplest formula based on elements and percentages"""
    return formula_from_mass(elements)


def formula_from_mass(elements: [(str, Measurement)], molar_mass = None) -> str:
#    _masses = [validate_measurement(mass, GRAMS) for (_, mass) in elements]
#    _elements = [element for (element, _) in elements]

    _elements = [element for (element, _) in elements]
    _masses = [moles_from_grams(grams(percent), element) for (element, percent) in elements]

    min_mass = min(_masses)

    _subscripts = []
    for mass in _masses:
        subscript = mass.value.decimal() / min_mass.value.decimal()
        subscript = round(subscript, 4)
        _subscripts.append(subscript)

    formula = ''
    _subscripts = _simplify(_subscripts)
    for element, subscript in zip(_elements, _subscripts):
        formula += element + (str(subscript) if subscript > 1 else '')

    if molar_mass:
        return mol_formula_from_simple_formula(formula, molar_mass)
    return formula

def mol_formula_from_simple_formula(simple: str, ex_molar_mass: Measurement) -> str:
    _ex_molar_mass = validate_measurement(ex_molar_mass, GRAMS / MOLES)
    _sm_molar_mass = molar_mass(simple)
    multiplier = int(_ex_molar_mass.value / _sm_molar_mass.value)
    simple_composition = composition(simple)
    return f'{(simple_composition * multiplier):f}'

def _simplify(numbers: [Decimal]) -> Decimal:

    _numbers = numbers[0:]
    with_decimal = [number for number in _numbers if number - int(number) >= 0.1]
    prevent_infinite = 0
    while (len(with_decimal) > 0 and prevent_infinite < 100):
        prevent_infinite += 1
        decimal_part = with_decimal[0] - int(with_decimal[0])
        multiplier = round(1 / decimal_part, 0)
        _numbers = [number * multiplier for number in _numbers]
        with_decimal = [number for number in _numbers if number - int(number) >= 0.1]

    return [round(number,0) for number in _numbers]
