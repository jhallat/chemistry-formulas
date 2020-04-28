from periodictable import PeriodicTable
from decimal import Decimal, getcontext

def composition(value):
    tokens = []
    current_token = ''
    for char in value:
        if char.isdigit() and current_token.isdigit():
            current_token += char
        elif char == char.upper() and len(current_token) > 0:
            tokens += [current_token]
            current_token = char
        else:
            current_token += char
    if len(current_token) > 0:
        tokens += [current_token]

    composition = []
    in_digit = False
    in_element = False
    count = ''
    element = ''
    for token in tokens:
        if (not in_digit) and (not in_element):
            # TODO raise an exception if the first character is a digit
            element += token
            in_element = True
        elif in_digit:
             composition += [(count, element)]
             element = token
             count = ''
             in_digit = False
             in_element = True
        elif in_element:
            if token.isdigit():
                count = token
                in_digit = True
                in_element = False
            else:
                composition += [(count if count else '1', element)]
                element = token
                count=''
    composition += [(count, element)]
    return composition

def sig_digits(value):
    svalue = str(value)
    digits = 0
    if '.' in svalue:
        digits = len(svalue) - 1
    else:
        zero = True
        for char in reversed(svalue):
            if not (zero and char == '0'):
                zero = False
                digits += 1
    return digits

def round_to_sig_digits(value, digits):
    svalue = str(value)
    adigits = digits + 1
    before_decimal = True
    leading_zeros = True
    nvalue = ''
    for char in svalue:
        if leading_zeros:
            if not char == '0':
                leading_zeros = False
            else:
                nvalue += '0'
                continue
        if not char == '.':
            if adigits > 0:
                nvalue += char
            else:
                if before_decimal:
                    nvalue += '0'
                else:
                    break
            adigits -= 1
        else:
            before_decimal = False
            nvalue += '.'
    # TODO need to properly round
    return Decimal(round_last(nvalue))

def round_last(value):
    str_value = str(value)
    decimal = '.' in str_value
    last = str_value[len(str_value) - 1]
    str_value = str_value[:-1]

    trail = ''

    if int(last) >= 5:
        if str_value[-1] == '9':
            while (str_value[-1] == '9' or str_value[-1] == '.') and len(str_value) > 1:
                if str_value[-1] == '.':
                    trail = '.' + trail
                    str_value = str_value[:-1]
                    continue
                trail = '0' + trail
                str_value = str_value[:-1]
        next_last = int(str_value[-1]) + 1
        str_value = str_value[:-1] + str(next_last) + trail
    if not decimal:
        str_value = str_value + '0'

    return Decimal(str_value)

def molar_mass(formula):
    table = PeriodicTable()
    atoms = composition(formula)
    total_mass = 0
    for count, symbol in atoms:
        mass = table.search(symbol).atomic_mass
        total_mass = total_mass + (Decimal(mass) * Decimal(count))
    return (total_mass, 'g/mol')

def moles_from_grams(grams, formula):
    mmass = molar_mass(formula)[0]
    digits = min(sig_digits(grams), sig_digits(mmass))
    value = round_to_sig_digits(Decimal(str(grams)) / molar_mass(formula)[0], digits)
    return (value, 'mol')

# TODO add a measurement class instead of using tuples !!!

if __name__ == '__main__':
    print(f"molar mass of 'K2CrO4' = {molar_mass('K2CrO4')}")
    print(f"molar mass of 'C12H22O11' = {molar_mass('C12H22O11')}")

    print(f"{moles_from_grams(212, 'K2CrO4')[0]} moles in 212g of K2Cr04")
    print(f"{moles_from_grams(212, 'C12H22O11')[0]} moles in 212g of C12H22O11")