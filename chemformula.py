from collections import namedtuple
from decimal import Decimal

from formulaparser import parse_formula
from measurement import Measurement, grams
from mole import molar_mass, moles_from_grams

Component = namedtuple("Component", "count symbol mass mass_percent")

def composition(formula: str, mass:Measurement = grams('1.000') ) -> [Component]:
    _composition = parse_formula(formula)
    _molar_mass = molar_mass(formula)
    _components = []
    for count, symbol in _composition:
        _mass_percent = molar_mass(symbol)/_molar_mass
        _mass_percent = _mass_percent.value.decimal() * int(count)
        _mass = mass * _mass_percent
        _mass_percent = round(_mass_percent * 100, 2)
        _components.append(Component(count, symbol, _mass, _mass_percent))

    return _components

def formula_from_percent(elements: [(str, Decimal)]) -> str:
    """Creates the simplest formula based on elements and percentages"""

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

    return formula

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
