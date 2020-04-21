from periodictable import PeriodicTable
from decimal import Decimal

def composition(value):
    tokens = []
    current_token = ''
    for char in value:
        if char == char.upper() and len(current_token) > 0:
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
            if token.isdigit():
                count += token
            else:
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

def molar_mass(value):
    table = PeriodicTable()
    atoms = composition(value)
    print(atoms)
    total_mass = 0
    for count, symbol in atoms:
        mass = table.search(symbol).atomic_mass
        print(f'{symbol} = {mass} * {count}')
        total_mass = total_mass + (Decimal(mass) * Decimal(count))
    return (total_mass, 'g/mol')


if __name__ == '__main__':
    print(molar_mass('K2CrO4'))
    print(molar_mass('C12H22O11'))