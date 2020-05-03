from decimal import Decimal

from chemformula import composition, sig_digits, round_to_sig_digits
from measurement import Measurement, GRAMS, MOLES, validate_measurement, LITERS
from periodictable import PeriodicTable


def molar_mass(formula):
    table = PeriodicTable()
    atoms = composition(formula)
    total_mass = 0
    digits = 0
    for count, symbol in atoms:
        mass = table.search(symbol).atomic_mass
        digits = sig_digits(mass) if digits == 0 else min(digits, sig_digits(mass))
        total_mass = total_mass + (Decimal(mass) * Decimal(count))
        total_mass = round_to_sig_digits(total_mass, digits)
    return Measurement(total_mass, GRAMS / MOLES)


def moles_from_grams(grams, formula):
    mmass = molar_mass(formula).value
    digits = min(sig_digits(grams), sig_digits(mmass))
    value = round_to_sig_digits(Decimal(str(grams)) / mmass, digits)
    return Measurement(value, MOLES)


def molarity(moles, liters=None):
    _moles = validate_measurement(moles, MOLES)
    if liters == None:
        return Measurement(_moles.value, MOLES / LITERS)

    _liters = validate_measurement(liters, LITERS)

    digits = min(sig_digits(moles), sig_digits(liters))
    molarity = round_to_sig_digits(_moles / _liters, digits)
    return molarity

def grams_in_solution(molarity: Measurement, molar_mass: Measurement, liters: Measurement) -> Measurement:
    """ Calculates the mass in grams of a compound in a solution  of a specified molarity
    """

    _molarity = validate_measurement(molarity, MOLES / LITERS)
    _molar_mass = validate_measurement(molar_mass, GRAMS / MOLES)
    _liters = validate_measurement(liters, LITERS)

    digits = min(sig_digits(_molarity), sig_digits(_molar_mass), sig_digits(_liters))
    return round_to_sig_digits(_liters * _molar_mass * _molarity, digits)


def molarity_of_solution(grams: Measurement, molar_mass: Measurement, liters:Measurement) -> Measurement:
    """ Calculates the molarity of a solution
    """

    _grams = validate_measurement(grams, GRAMS)
    _molar_mass = validate_measurement(molar_mass, GRAMS / MOLES)
    _liters = validate_measurement(liters, LITERS)

    digits = min(sig_digits(_grams), sig_digits(_molar_mass))
    _moles = round_to_sig_digits(_grams / _molar_mass, digits)
    digits = min(digits, sig_digits(_liters))

    return round_to_sig_digits(_moles / _liters, digits)


def moles_in_solution(molarity, liters):
    """Finds the number of moles in a solution of a specified molarity
    """

    _molarity = validate_measurement(molarity, MOLES / LITERS)
    _liters = validate_measurement(liters, LITERS)

    digits = min(sig_digits(_molarity), sig_digits(_liters))
    return round_to_sig_digits(_molarity * _liters, digits)


def volume_from_solution(moles: Measurement, molarity: Measurement) -> Measurement:
    """Finds the volume of a solution that will contain the specified number of moles when taken
       from a solution of a specified molarity
    """

    _moles = validate_measurement(moles, MOLES)
    _molarity = validate_measurement(molarity, MOLES / LITERS)

    digits = min(sig_digits(_moles), sig_digits(_molarity))
    return round_to_sig_digits(_moles / _molarity, digits)

