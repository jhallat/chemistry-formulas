from decimal import Decimal
from enum import Enum


class _FormulaTokenType(Enum):
    SYMBOL = 1
    SUBSCRIPT = 2
    COEFFICIENT = 3
    COMBINDED_WITH = 4

class _FormulaToken:
    """ Identifies the value and type of a formula token.
        Intended for internal use only!
    """

    def __init__(self, type: _FormulaTokenType, value: str):
        self.type = type
        self.value = value

    def __str__(self):
        return f'({self.type} : {self.value})'

class FormulaParseError(Exception):
    pass

def _tokenize(formula: str) -> [_FormulaToken]:

    STATE_START = 1
    STATE_COEFFICIENT = 2
    STATE_SYMBOL = 3
    STATE_EXPECT_SYMBOL = 4
    STATE_SUBSCRIPT = 5

    tokens = []
    token = ''
    state = STATE_START
    for pos,char in enumerate(formula):

        if state == STATE_START:
            if char == '[':
                state = STATE_COEFFICIENT
            elif char.isalpha():
                token = char
                state = STATE_SYMBOL
            else:
                raise FormulaParseError(f'invalid character {char} at position {pos}')
            continue
        elif state == STATE_COEFFICIENT:
            if char.isdigit() or char == '/':
                token += char
            if char == ']':
                if len(token) == 0:
                    raise FormulaParseError(f'missing coefficient at position {pos}')
                else:
                    if '/' in token:
                        numbers = token.split('/')
                        token = str(round(Decimal(numbers[0])/Decimal(numbers[1]),3))
                    tokens.append(_FormulaToken(_FormulaTokenType.COEFFICIENT, token))
                    token = ''
                    state = STATE_EXPECT_SYMBOL
            continue
        elif state == STATE_SYMBOL:
            if char.isalpha():
                if char.isupper():
                    tokens.append(_FormulaToken(_FormulaTokenType.SYMBOL, token))
                    token = char
                else:
                    token += char
            elif char.isdigit():
                tokens.append(_FormulaToken(_FormulaTokenType.SYMBOL, token))
                token = char
                state = STATE_SUBSCRIPT
            elif char == '*':
                tokens.append(_FormulaToken(_FormulaTokenType.SYMBOL, token))
                tokens.append(_FormulaToken(_FormulaTokenType.COMBINDED_WITH, '*'))
                token = ''
                state = STATE_START
            continue
        elif state == STATE_EXPECT_SYMBOL:
            if char.isalpha():
                token = char
                state = STATE_SYMBOL
            else:
                raise FormulaParseError(f'invalid character {char} at position {pos}')
            continue
        elif state == STATE_SUBSCRIPT:
            if char.isdigit():
                token += char
            elif char.isalpha():
                tokens.append(_FormulaToken(_FormulaTokenType.SUBSCRIPT, token))
                token = char
                state = STATE_SYMBOL
            elif char == '*':
                tokens.append(_FormulaToken(_FormulaTokenType.SUBSCRIPT, token))
                tokens.append(_FormulaToken(_FormulaTokenType.COMBINDED_WITH, '*'))
                token = ''
                state = STATE_START

    if len(token) > 0:
        if state == STATE_SUBSCRIPT:
            tokens.append(_FormulaToken(_FormulaTokenType.SUBSCRIPT, token))
        elif state == STATE_SYMBOL:
            tokens.append(_FormulaToken(_FormulaTokenType.SYMBOL, token))
        else:
            raise FormulaParseError(f'unexpected formula termination')

    return tokens

def _reduce(elements: [(Decimal, str)]) -> [(Decimal, str)]:
    element_map = {}
    reduced_elements = []
    for element in elements:
        if element[1] in element_map:
            current = element_map[element[1]]
            current += element[0]
            element_map[element[1]] = current
        else:
            element_map[element[1]] = element[0]

    for element in elements:
        if element[1] in element_map:
            reduced_elements.append((element_map[element[1]], element[1]))
            del element_map[element[1]]

    return reduced_elements

#TODO add a precision parameter for multiply coefficient with subscript. Default = 3
def parse_formula(formula: str) -> (str, str):

    STATE_START = 1
    STATE_COEFFICIENT = 2
    STATE_SYMBOL = 3
    STATE_SUBSCRIPT = 4

    tokens = _tokenize(formula)
    elements = []
    state = STATE_START
    coefficient = Decimal('1.000')
    symbol = ''
    for token in tokens:
        if state == STATE_START:
            if token.type == _FormulaTokenType.COEFFICIENT:
                coefficient = Decimal(token.value)
                state = STATE_COEFFICIENT
            elif token.type == _FormulaTokenType.SYMBOL:
               symbol = token.value
               state = STATE_SYMBOL
            else:
                raise FormulaParseError(f"expected coefficient or symbol at token '{token.value}'")
            continue
        if state == STATE_COEFFICIENT:
            if token.type == _FormulaTokenType.SYMBOL:
                symbol = token.value
                state = STATE_SYMBOL
            else:
                raise FormulaParseError(f"expected symbol at token '{token.value}'")
            continue
        if state == STATE_SYMBOL:
            if token.type == _FormulaTokenType.SYMBOL:
                elements.append((coefficient, symbol))
                symbol = token.value
            elif token.type == _FormulaTokenType.SUBSCRIPT:
                amount = coefficient * Decimal(token.value)
                elements.append((amount, symbol))
                symbol = ''
                state = STATE_SUBSCRIPT
            elif token.type == _FormulaTokenType.COMBINDED_WITH:
                elements.append((coefficient, symbol))
                symbol = ''
                coefficient = Decimal('1.000')
                state = STATE_START
            else:
                raise FormulaParseError(f"expected symbol, subscript or '*' at token '{token.value}'")
            continue
        if state == STATE_SUBSCRIPT:
            if token.type == _FormulaTokenType.SYMBOL:
                symbol = token.value
                state = STATE_SYMBOL
            elif token.type == _FormulaTokenType.COMBINDED_WITH:
                symbol = ''
                coefficient = Decimal('1.000')
                state = STATE_START
            else:
                raise FormulaParseError(f"expected symbol or '*' at token '{token.value}'")

    if len(symbol) > 0 and state == STATE_SYMBOL:
        elements.append((coefficient, symbol))

    return _reduce(elements)

