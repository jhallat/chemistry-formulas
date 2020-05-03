from measurement import Measurement, GRAMS, MOLES, validate_measurement, LITERS
from periodictable import PeriodicTable
from decimal import Decimal


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
    composition += [(count if count else '1', element)]
    return composition

def sig_digits(value):
    if isinstance(value, Measurement):
        svalue = str(value.value)
    else:
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
    if isinstance(value, Measurement):
        svalue = str(value.value)
    else:
        svalue = str(value)
    adigits = digits + 1
    before_decimal = True
    leading_zeros = True
    nvalue = ''
    for char in svalue:
        if leading_zeros and not char == '.':
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
            if adigits > 0:
                nvalue += '.'
            else:
                break
    if adigits > 0 and not before_decimal:
        nvalue = nvalue + ('0' * adigits)
    # TODO need to properly round
    rounded_value = Decimal(round_last(nvalue))
    if isinstance(value, Measurement):
        return Measurement(rounded_value, value.unit)
    else:
        return Decimal(Decimal(round_last(nvalue)))

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
        last = str_value[-1]
        str_value = str_value[:-1] + str(next_last) + trail
    if not decimal:
        trail = ''
        if last == '0':
            while last == '0':
                trail += '0';
                last = str_value[-1]
                str_value = str_value[:-1]

        str_value = str_value + '0' + trail

    return Decimal(str_value)



