from _decimal import Decimal
from enum import Enum

class FormulaTokenizeError(Exception):
    pass

class FormulaTokenType(Enum):
    SYMBOL = 1
    SUBSCRIPT = 2
    COEFFICIENT = 3
    COMBINDED_WITH = 4
    POLYATOMIC_START = 5
    POLYATOMIC_END = 6

class TokenState(Enum):
    START = 1
    COEFFICIENT = 2
    SYMBOL = 3
    EXPECT_SYMBOL = 4
    SUBSCRIPT = 5
    POLYATOMIC_END = 6

class FormulaToken:
    """ Identifies the value and type of a formula token.
        Intended for internal use only!
    """

    def __init__(self, type: FormulaTokenType, value: str):
        self.type = type
        self.value = value

    def __repr__(self):
        return f'({self.type} : {self.value})'

def state_start(pos, char, tokens, polyatomic):
    if char == '[':
        token = ''
        state = TokenState.COEFFICIENT
    elif char.isalpha():
        token = char
        state = TokenState.SYMBOL
    elif char == '(':
        token = ''
        tokens.append(FormulaToken(FormulaTokenType.POLYATOMIC_START, '('))
        state = TokenState.START
        polyatomic = True
    else:
        raise FormulaTokenizeError(f'invalid character {char} at position {pos}')
    return state, token, tokens, polyatomic

def state_coefficient(pos, char, token, tokens):
    state = TokenState.COEFFICIENT
    if char.isdigit() or char == '/':
        token += char
    if char == ']':
        if len(token) == 0:
            raise FormulaTokenizeError(f'missing coefficient at position {pos}')
        else:
            if '/' in token:
                numbers = token.split('/')
                token = str(round(Decimal(numbers[0]) / Decimal(numbers[1]), 3))
            tokens.append(FormulaToken(FormulaTokenType.COEFFICIENT, token))
            token = ''
            state = TokenState.EXPECT_SYMBOL
    return state, token, tokens


def state_symbol(pos, char, token, tokens, polyatomic):
    if char.isalpha():
        if char.isupper():
            tokens.append(FormulaToken(FormulaTokenType.SYMBOL, token))
            token = char
        else:
            token += char
        state = TokenState.SYMBOL
    elif char.isdigit():
        tokens.append(FormulaToken(FormulaTokenType.SYMBOL, token))
        token = char
        state = TokenState.SUBSCRIPT
    elif char == '*':
        tokens.append(FormulaToken(FormulaTokenType.SYMBOL, token))
        tokens.append(FormulaToken(FormulaTokenType.COMBINDED_WITH, '*'))
        token = ''
        state = TokenState.START
    elif char == '(':
        tokens.append(FormulaToken(FormulaTokenType.SYMBOL, token))
        tokens.append(FormulaToken(FormulaTokenType.POLYATOMIC_START, '('))
        token = ''
        polyatomic = True
        state = TokenState.START
    elif char == ')':
        if polyatomic:
            tokens.append(FormulaToken(FormulaTokenType.SYMBOL, token))
            tokens.append(FormulaToken(FormulaTokenType.POLYATOMIC_END, ')'))
            token = ''
            polyatomic = False
            state = TokenState.POLYATOMIC_END
        else:
            raise FormulaTokenizeError(f'invalid character {char} at position {pos}')
    else:
        raise FormulaTokenizeError(f'invalid character {char} at position {pos}')
    return state, token, tokens, polyatomic


def state_expect_symbol(pos, char):
    if char.isalpha():
        token = char
        state = TokenState.SYMBOL
    else:
        raise FormulaTokenizeError(f'invalid character {char} at position {pos}')
    return state, token


def state_subscript(pos, char, token, tokens, polyatomic):
    if char.isdigit():
        token += char
        state = TokenState.SUBSCRIPT
    elif char.isalpha():
        tokens.append(FormulaToken(FormulaTokenType.SUBSCRIPT, token))
        token = char
        state = TokenState.SYMBOL
    elif char == '*':
        tokens.append(FormulaToken(FormulaTokenType.SUBSCRIPT, token))
        tokens.append(FormulaToken(FormulaTokenType.COMBINDED_WITH, '*'))
        token = ''
        state = TokenState.START
    elif char == '(':
        tokens.append(FormulaToken(FormulaTokenType.SUBSCRIPT, token))
        tokens.append(FormulaToken(FormulaTokenType.POLYATOMIC_START, '('))
        token = ''
        polyatomic = True
        state = TokenState.START
    elif char == ')':
        if polyatomic:
            tokens.append(FormulaToken(FormulaTokenType.SUBSCRIPT, token))
            tokens.append(FormulaToken(FormulaTokenType.POLYATOMIC_END, ')'))
            token = ''
            polyatomic = False
            state = TokenState.POLYATOMIC_END
        else:
            raise FormulaTokenizeError(f'invalid character {char} at position {pos}')
    else:
        raise FormulaTokenizeError(f'invalid character {char} at position {pos}')
    return state, token, tokens, polyatomic


def state_polyatomic_end(pos, char, tokens):
    polyatomic = False
    if char.isalpha():
        token = char
        state = TokenState.SYMBOL
    if char.isdigit():
        token = char
        state = TokenState.SUBSCRIPT
    elif char == '*':
        tokens.append(FormulaToken(FormulaTokenType.COMBINDED_WITH, '*'))
        token = ''
        state = TokenState.START
    elif char == '(':
        tokens.append(FormulaToken(FormulaTokenType.POLYATOMIC_START, '('))
        token = ''
        polyatomic = True
        state = TokenState.START
    else:
        raise FormulaTokenizeError(f'invalid character {char} at position {pos}')
    return state, token, tokens, polyatomic


def tokenize(formula: str) -> [FormulaToken]:
    tokens = []
    token = ''
    state = TokenState.START
    polyatomic = False
    for pos, char in enumerate(formula):
        if state == TokenState.START:
            state, token, tokens, polyatomic = state_start(pos, char, tokens, polyatomic)
        elif state == TokenState.COEFFICIENT:
            state, token, tokens = state_coefficient(pos, char, token, tokens)
        elif state == TokenState.SYMBOL:
            state, token, tokens, polyatomic = state_symbol(pos, char, token, tokens, polyatomic)
        elif state == TokenState.EXPECT_SYMBOL:
            state, token = state_expect_symbol(pos, char)
        elif state == TokenState.SUBSCRIPT:
            state, token, tokens, polyatomic = state_subscript(pos, char, token, tokens, polyatomic)
        elif state == TokenState.POLYATOMIC_END:
            state, token, tokens, polyatomic = state_polyatomic_end(pos, char, tokens)

    if len(token) > 0:
        if state == TokenState.SUBSCRIPT:
            tokens.append(FormulaToken(FormulaTokenType.SUBSCRIPT, token))
        elif state == TokenState.SYMBOL:
            tokens.append(FormulaToken(FormulaTokenType.SYMBOL, token))
        else:
            raise FormulaTokenizeError(f'unexpected formula termination')

    return tokens