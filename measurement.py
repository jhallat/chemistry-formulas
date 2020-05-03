from decimal import Decimal

class InvalidUnitError(Exception):
    pass


class Unit(object):

    __slots__ = ("value")

    def __init__(self, value):
        if isinstance(value, Unit):
            object.__setattr__(self, "value", value.value)
        else:
            object.__setattr__(self, "value", value)

    def __setattr__(self, *args):
        raise AttributeError("Unit is immutable")

    def __delattr__(self, *args):
        raise AttributeError("Unit is immutable")


    def __str__(self):
        return self.value

    def __truediv__(self, other):
        return self * self._reciprocal(other)

    def __eq__(self, other):
        return self.value == other.value

    def __mul__(self, other):
        multiplicand = self.value.split('/')
        multiplier = other.value.split('/')

        if len(multiplicand) == 1:
            multiplicand += '1'

        if len(multiplier) == 1:
           multiplier += '1'

        numerator = multiplier[0].split('*')
        numerator += multiplicand[0].split('*')
        denominator = multiplier[1].split('*')
        denominator += multiplicand[1].split('*')

        simp_num = [i for i in numerator if i not in denominator]
        simp_den = [i for i in denominator if i not in numerator and not i == '1']

        return Unit('*'.join(simp_num) + '/' + '*'.join(simp_den)) if len(simp_den) > 0 else Unit('*'.join(simp_num))

    def _reciprocal(self, unit):
        if '/' in unit.value:
            fraction = unit.value.split('/')
            return Unit(fraction[1] + '/' + fraction[0])
        else:
            return Unit('1/' + unit.value)


GRAMS = Unit('g')
LITERS = Unit('L')
MOLES = Unit('mol')

# TODO Convenience methods for measurements
class Measurement:

    def __init__(self, value, unit):
        self.value = Decimal(value)
        self.unit = Unit(unit)

    def __str__(self):
        return str(self.value) + ' ' + str(self.unit)

    def __eq__(self, other):
        if not isinstance(other, Measurement):
            return False
        return self.value == other.value and self.unit == other.unit

    def __truediv__(self, other):
        if isinstance(other, int):
            return Measurement(self.value / other, self.unit)

        div_value = self.value / other.value
        div_unit = self.unit / other.unit
        return Measurement(div_value, div_unit)

    def __mul__(self, other):
        mul_value = self.value * other.value
        mul_unit = self.unit * other.unit
        return Measurement(mul_value, mul_unit)

def validate_measurement(value, unit):
    if isinstance(value, Measurement):
        if value.unit == Unit(unit):
            return value
        else:
            raise InvalidUnitError(f"Expected unit: '{unit}', received: '{value.unit}'")
    return Measurement(Decimal(value), unit)

def grams(value):
    return Measurement(Decimal(value), GRAMS)

def liters(value):
    return Measurement(Decimal(value), LITERS)

def moles(value):
    return Measurement(Decimal(value), MOLES)

def milli(value):
    if not isinstance(value, Measurement):
        raise InvalidUnitError("milli() requires a Measurement object as first parameter")
    return value / 1000